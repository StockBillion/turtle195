#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy
import pandas as pf
import tushare as ts
from matplotlib.pylab import date2num, num2date
import datetime


# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

def parse_stock_data(stock_data):
    data_list = []
    ave_price = []
    volumes = []

    for rnum, row in stock_data.iterrows():
        tscode, trade_date, open, close, high, low = row[0:6]
        vol,amount = row[9:11]
        _date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        timenum = date2num(_date)

        datas = (timenum, open, high, low, close)
        data_list.append(datas)
        ave_price.append( (high+low)/2 )
        volumes.append(vol)

    data_table = numpy.transpose( data_list )
    dates = data_table[0]
    return dates, data_list, ave_price, volumes

class StockDataSet:
    '股票数据集合'
    stocks = {}
    
    def _join(self, csv_data2, net_data1):
        len1 = len(net_data1)
        len2 = len(csv_data2)
        print('join csv_data', len2, ' net_data1', len1)

        if len1 < 1: 
            return csv_data2
        if len2 < 1: 
            return net_data1

        _head1 = net_data1.at[0, 'trade_date']
        _head2 = csv_data2.at[0, 'trade_date']
        _tear1 = net_data1.at[len1-1, 'trade_date']
        _tear2 = csv_data2.at[len2-1, 'trade_date']

        if _head1 < _head2:
            if _tear1 < _tear2:
                temp = csv_data2.loc[csv_data2['trade_date'] > _head1]
                data0 = temp.append(net_data1, ignore_index=True)
            else:
                data0 = csv_data2
        elif _head1 > _head2:
            if _tear1 < _tear2:
                data0 = net_data1
            else:
                temp = net_data1.loc[net_data1['trade_date'] > _head1]
                data0 = temp.append(csv_data2, ignore_index=True)
        else:
            if _tear1 < _tear2:
                data0 = net_data1
            else:
                data0 = csv_data2

        return data0

    def _read(self, code, time_unit = 'daily'):
        try:
            self.stocks[code] = pf.read_csv('./data/' + code + '.' + time_unit + '.csv', 
                index_col=0, dtype = {'trade_date' : str})
            return self.stocks[code]
        except IOError: 
            return pf.DataFrame()

    def _daily2weekly(self, daily_datas):
        weekly_datas = pf.DataFrame()
        kidx = 0
        start = 0
        
        for rnum, row in daily_datas.iterrows():
            ts_code, trade_date, open, close, high, low = row[0:6]
            pre_close,change,pct_chg,vol,amount = row[6:11]
            _date = datetime.datetime.strptime(trade_date, '%Y%m%d')
            _weekday = _date.weekday()

            if _weekday == 0:
                if start:
                    _row = {'ts_code': [ts_code], 'trade_date': [trade_date], 
                        'open': [_open], 'close': [_close], 'high': [_high], 'low': [_low], 
                        'pre_close': [pre_close], 'change': [change], 'pct_chg': [pct_chg], 
                        'vol': [_vol], 'amount': [_amount]}
                    _index = [kidx]
                    weekly_datas = weekly_datas.append(pf.DataFrame(_row, _index))
                    kidx = kidx+1

                start = 1
                _open = open
                _close = close
                _high = high
                _low = low
                _vol = vol
                _amount = amount

            elif start:
                _close = close
                _high = max(_high, high)
                _low = min(_low, low)
                _vol += vol
                _amount += amount

        return weekly_datas


    def _download(self, code, startdate, enddate, stype, time_unit = 'daily'):
        print('download ', stype, ' ', code, ' data, from ', startdate, ' to ', enddate)
        startdate = str(startdate)
        enddate = str(enddate)

        if stype == 'index':
            hist_data = pro.index_daily(ts_code=code, start_date=startdate, end_date=enddate)
            if time_unit == 'weekly':
                hist_data = self._daily2weekly(hist_data)
            elif time_unit == 'monthly':
                hist_data = self._daily2monthly(hist_data)

        elif stype == 'fund':
            hist_data = pro.fund_daily(ts_code=code, start_date=startdate, end_date=enddate)
            if time_unit == 'weekly':
                hist_data = self._daily2weekly(hist_data)
            elif time_unit == 'monthly':
                hist_data = self._daily2monthly(hist_data)

        else:
            if time_unit == 'daily':
                hist_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
            elif time_unit == 'weekly':
                hist_data = pro.weekly(ts_code=code, start_date=startdate, end_date=enddate)
            elif time_unit == 'monthly':
                hist_data = pro.monthly(ts_code=code, start_date=startdate, end_date=enddate)

        print('download', len(hist_data), 'row data')
        return hist_data

    def load(self, code, startdate, enddate, stype = 'stock', time_unit = 'daily'):
        print('download', stype, code, time_unit, 'data, from', startdate, 'to', enddate)

        if startdate is not numpy.int64:
            startdate = numpy.int64(startdate)
        if enddate is not numpy.int64:
            enddate = numpy.int64(enddate)

        local_data = self._read(code, time_unit)
        _rowcount = len(local_data)
        
        if _rowcount > 0 :
            _head = numpy.int64(local_data.at[0, 'trade_date'])
            _tear = numpy.int64(local_data.at[_rowcount-1, 'trade_date'])

            if _head+1 < enddate:
                down_data = self._download(code, _head + 1, enddate, stype, time_unit)
                local_data = self._join(local_data, down_data)
            if _tear-1 > startdate:
                down_data = self._download(code, startdate, _tear-1, stype, time_unit)
                local_data = self._join(local_data, down_data)
        else:
            down_data = self._download(code, startdate, enddate, stype, time_unit)
            local_data = down_data

        if len(local_data) > _rowcount:
            print('write csv file', len(local_data), 'rows')
            local_data.to_csv('./data/' + code + '.' + time_unit + '.csv')
        self.stocks[code] = local_data.sort_index(ascending=False)
        

if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20180101'
    enddate = '20181201'
    stype = 'stock'

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument('filename', default=['601857.sh'], nargs='*')
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")
    parser.add_argument("-t", "--data_type", help="end date")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = ARGS.start_date
    if ARGS.end_date:
        enddate = ARGS.end_date
    if ARGS.data_type:
        stype = str(ARGS.data_type)
    if ARGS.filename:
        stock_codes = ARGS.filename

    for code in stock_codes:
        dataset.load(code, startdate, enddate, stype)



        # if time_unit == 'daily':
        #     if stype == 'index':
        #         hist_data = pro.index_daily(ts_code=code, start_date=startdate, end_date=enddate)
        #     elif stype == 'fund':
        #         hist_data = pro.fund_daily(ts_code=code, start_date=startdate, end_date=enddate)
        #     else:
        #         hist_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
        # elif time_unit == 'weekly':
        #     if stype == 'index':
        #         hist_data = pro.index_daily(ts_code=code, start_date=startdate, end_date=enddate)
        #         hist_data = self._daily2weekly(hist_data)
        #         # hist_data = pro.index_weekly(ts_code=code, start_date=startdate, end_date=enddate)
        #     elif stype == 'fund':
        #         hist_data = self._daily2monthly(hist_data)
        #         # hist_data = pro.fund_weekly(ts_code=code, start_date=startdate, end_date=enddate)
        #     # else:
        #         # hist_data = pro.weekly(ts_code=code, start_date=startdate, end_date=enddate)
        # elif time_unit == 'monthly':
        #     hist_data = pro.fund_daily(ts_code=code, start_date=startdate, end_date=enddate)
        #     if stype == 'index':
        #         # hist_data = pro.index_monthly(ts_code=code, start_date=startdate, end_date=enddate)
        #     elif stype == 'fund':
        #         # hist_data = pro.fund_monthly(ts_code=code, start_date=startdate, end_date=enddate)
        #     # else:
        #         # hist_data = pro.monthly(ts_code=code, start_date=startdate, end_date=enddate)
