#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy
import pandas as pf
import tushare as ts


# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

class StockDataSet:
    '股票数据集合'
    stocks = {}
    
    def join(self, csv_data2, net_data1):
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
                # print("temp len", len(temp))
                data0 = temp.append(net_data1, ignore_index=True)
                # print("net_data1 len", len(net_data1))
                # print("data0 len", len(data0))
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

    def read(self, code):
        try:
            self.stocks[code] = pf.read_csv('./data/' + code + '.csv', index_col=0, dtype = {'trade_date' : str})
            return self.stocks[code]
        except IOError: 
            return pf.DataFrame()

    def daily(self, code, startdate, enddate, stype):
        print('download ', stype, ' ', code, ' data, from ', startdate, ' to ', enddate)
        startdate = str(startdate)
        enddate = str(enddate)

        if stype == 'index':
            hist_data = pro.index_daily(ts_code=code, start_date=startdate, end_date=enddate)
        elif stype == 'fund':
            hist_data = pro.fund_daily(ts_code=code, start_date=startdate, end_date=enddate)
        else:
            hist_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)

        print('download', len(hist_data), 'row data')
        # hist_data.info()
        return hist_data

    def load(self, code, startdate, enddate, stype = 'stock'):
        print('download ', stype, ' ', code, ' data, from ', startdate, ' to ', enddate)

        if startdate is not numpy.int64:
            startdate = numpy.int64(startdate)
        if enddate is not numpy.int64:
            enddate = numpy.int64(enddate)

        local_data = self.read(code)
        _rowcount = len (local_data)
        
        if _rowcount > 0 :
            _head = numpy.int64(local_data.at[0, 'trade_date'])
            _tear = numpy.int64(local_data.at[_rowcount-1, 'trade_date'])

            if _head+1 < enddate:
                down_data = self.daily(code, _head + 1, enddate, stype)
                local_data = self.join(local_data, down_data)
            if _tear-1 > startdate:
                down_data = self.daily(code, startdate, _tear-1, stype)
                local_data = self.join(local_data, down_data)
        else:
            down_data = self.daily(code, startdate, enddate, stype)
            local_data = down_data

        if len(local_data) > _rowcount:
            print('write csv file', len(local_data), 'rows')
            local_data.to_csv('./data/' + code + '.csv')
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


        # local_data.info()
        # print(len)
        # print(local_data)
        # print(local_data.at[ 0, 'trade_date'])
        # print(local_data.at[50, 'trade_date'])
        # print(local_data.at[90, 'trade_date'])
        # print(local_data.at[_rowcount-1, 'trade_date'])

        # print(type(net_data1.at[0, 'trade_date']))
        # print(type(csv_data2.at[0, 'trade_date']))

        # print(type(data1.at[0, 'trade_date']))
        # print(type(data2.at[0, 'trade_date']))

                # data1['trade_date'].info()
        # print( 'load stock ' + code + ' data')
        # data2.at[0, 'trade_date'].info()
                # down_data = pro.daily(ts_code=code, start_date=startdate, end_date=_tear)
            # local_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
                # down_data = pro.daily(ts_code=code, start_date=str(local_data.at[ 0, 'trade_date'] + 1), 
                # end_date=enddate)

    # opts,args = getopt.getopt(sys.argv[1:], "e:hs:v", ['end=', 'help', 'start=', 'version'])
    # # opts, args = getopt.getopt(sys.argv[1:], "hvs:e:", ['help', 'version', 'start=', 'end='])
    # print(sys.argv[1:])
    # print(opts)

    # for opt_name, opt_value in opts:
    #     print(opt_name)
    #     print(opt_value)
    #     if opt_name in ('-h','--help'):
    #         sys.exit()
    #     elif opt_name in ('-v','--version'):
    #         sys.exit()
    #     elif opt_name in ('-s','--start'):
    #         startdate = opt_value
    #     elif opt_name in ('-e','--end'):
    #         enddate = opt_value

    # print(code)
    # print(startdate)
    # print(enddate)


        # down_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
        # self.stocks[code] = self.join(local_data, down_data)
        # down_data = down_data.sort_index(ascending=False)
        # down_data.to_csv('./data/' + code + '.csv')
        # self.stocks[code] = down_data

# import sys, getopt

            # print(_head)
            # type(_head)

            # print(enddate)
            # type(enddate)
