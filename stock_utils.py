#!/usr/bin/env python
#-*- coding: utf8 -*-
import numpy as np, pandas as pf, math, datetime as dt, time 
from matplotlib.pylab import date2num, num2date
import matplotlib.pyplot as plt, mpl_finance as mpf, tushare as ts


class StockDisp:
    '股票数据可视化'
    
    def __init__(self, title, xlabel='date', ylabel='price'):
        self.fig, [self.ax1, self.ax2] = plt.subplots(2,1,sharex=True)
        self.fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)

        plt.xticks(rotation=45)
        plt.yticks()
        plt.xlabel(xlabel)

        self.ax1.xaxis_date()
        self.ax1.set_title(title)
        self.ax1.set_ylabel(ylabel)

    def show(self):
        plt.grid()
        plt.show()

    def save(self, filename):
        plt.savefig(filename)


    def LogKDisp(self, ax1, data_list):
        data_table = np.transpose( data_list )
        data_table[1] = list(map(lambda x: math.log(x), data_table[1]))
        data_table[2] = list(map(lambda x: math.log(x), data_table[2]))
        data_table[3] = list(map(lambda x: math.log(x), data_table[3]))
        data_table[4] = list(map(lambda x: math.log(x), data_table[4]))

        data_list = np.transpose( data_table )
        mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')

    def LogPlot(self, ax1, dates, vals, _color='r', shift = 0, _label='label'):
        vals = list(map(lambda x: math.log(x)-shift, vals))
        ax1.plot(dates, vals, color=_color, lw=2, label=_label)

    def KDisp(self, ax1, data_list):
        mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='red', colordown='green')


    def Plot(self, ax1, dates, vals, _color='r', _label='label'):
        ax1.plot(dates, vals, color=_color, lw=2, label=_label)



class StockDataSet:
    '股票数据集合'
    
    # https://tushare.pro/
    ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
    pro = ts.pro_api()

    def __init__(self):
        self.stocks = {}


    def parse_data(self, code):
        if code not in self.stocks:
            return []
        stock_data = self.stocks[code]

        data_list = []
        ave_price = []
        volumes = []

        for rnum, row in stock_data.iterrows():
            tscode, trade_date, close, open, high, low = row[0:6]
            vol,amount = row[9:11]
            _date = dt.datetime.strptime(trade_date, '%Y%m%d')
            timenum = date2num(_date)

            datas = (timenum, open, high, low, close)
            data_list.append(datas)
            ave_price.append( (high+low)/2 )
            volumes.append(vol)

        data_table = np.transpose( data_list )
        dates = data_table[0]
        return dates, data_list, ave_price, volumes


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
        # return pf.DataFrame()
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
            ts_code, trade_date, close, open, high, low = row[0:6]
            # vol,amount = row[9:11]./
            pre_close,change,pct_chg,vol,amount = row[6:11]
            _date = dt.strptime(trade_date, '%Y%m%d')
            _weekday = _date.weekday()

            if _weekday == 0:
                if start:
                    _row = {'ts_code': [ts_code], 'trade_date': [_trade_date], 
                        'open': [_open], 'close': [_close], 'high': [_high], 'low': [_low], 
                        'pre_close': [pre_close], 'change': [change], 'pct_chg': [pct_chg], 
                        'vol': [_vol], 'amount': [_amount]}
                    _index = [kidx]
                    weekly_datas = weekly_datas.append(pf.DataFrame(_row, _index))
                    kidx = kidx+1

                start = 1
                _trade_date = trade_date
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

    @staticmethod
    def float_date(_date):
        if isinstance(_date, np.int64):
            _date = str(_date)
        if isinstance(_date, str):
            _date = dt.datetime.strptime(_date, '%Y%m%d')
        if isinstance(_date, dt.datetime):
            _date = date2num(_date)
        return _date

    @staticmethod
    def str_date(_date):
        if isinstance(_date, float):
            _date = num2date(_date).strftime('%Y%m%d')
        elif isinstance(_date, np.int64):
            _date = str(_date)
        elif isinstance(_date, dt.datetime):
            _date = _date.strftime('%Y%m%d')
        return _date

    @staticmethod
    def datetime(_date):
        if isinstance(_date, float):
            _date = num2date(_date)
        elif isinstance(_date, np.int64):
            _date = str(_date)
        if isinstance(_date, str):
            _date = dt.datetime.strptime(_date, '%Y%m%d')
        return _date


    def _download(self, code, startdate, enddate, stype, time_unit = 'daily'):
        print('download', stype, code, 'data, from', startdate, 'to', enddate)
        time.sleep(0.01)
        startdate = StockDataSet.str_date(startdate)
        enddate = StockDataSet.str_date(enddate)

        if stype == 'index':
            hist_data = StockDataSet.pro.index_daily(ts_code=code, start_date=startdate, end_date=enddate)
            if time_unit == 'weekly':
                hist_data = self._daily2weekly(hist_data)
            # elif time_unit == 'monthly':
            #     hist_data = self._daily2monthly(hist_data)

        elif stype == 'fund':
            hist_data = StockDataSet.pro.fund_daily(ts_code=code, start_date=startdate, end_date=enddate)
            if time_unit == 'weekly':
                hist_data = self._daily2weekly(hist_data)
            # elif time_unit == 'monthly':
            #     hist_data = self._daily2monthly(hist_data)

        else:
            if time_unit == 'daily':
                hist_data = StockDataSet.pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
            elif time_unit == 'weekly':
                hist_data = StockDataSet.pro.weekly(ts_code=code, start_date=startdate, end_date=enddate)
            elif time_unit == 'monthly':
                hist_data = StockDataSet.pro.monthly(ts_code=code, start_date=startdate, end_date=enddate)

        print('download', len(hist_data), 'row data')
        return hist_data

    def load(self, code, startdate, enddate, stype = 'stock', time_unit = 'daily'):
        print('load', stype, code, time_unit, 'data, from', startdate, 'to', enddate)

        startdate = StockDataSet.float_date(startdate)
        enddate = StockDataSet.float_date(enddate)
        # if startdate is not np.int64:
        #     startdate = np.int64(startdate)
        # if enddate is not np.int64:
        #     enddate = np.int64(enddate)

        local_data = self._read(code, time_unit)
        _rowcount = len(local_data)
        
        if _rowcount > 0:
            _head = StockDataSet.float_date(local_data.at[0, 'trade_date'])
            _tear = StockDataSet.float_date(local_data.at[_rowcount-1, 'trade_date'])
            
            # _head = np.int64(local_data.at[0, 'trade_date'])
            # _tear = np.int64(local_data.at[_rowcount-1, 'trade_date'])
            # print(_head, _tear, enddate, startdate)
            # print(enddate - _head, _tear - startdate)

            if enddate - _head > 10: #_head+1 < enddate:
                down_data = self._download(code, _head + 1, enddate, stype, time_unit)
                local_data = self._join(local_data, down_data)
            if _tear - startdate > 10: #_tear-1 > startdate:
                down_data = self._download(code, startdate, _tear-1, stype, time_unit)
                local_data = self._join(local_data, down_data)
        else:
            down_data = self._download(code, startdate, enddate, stype, time_unit)
            local_data = down_data

        if len(local_data) > _rowcount:
            print('write csv file', len(local_data), 'rows')
            local_data.to_csv('./data/' + code + '.' + time_unit + '.csv')

        self.stocks[code] = local_data.sort_index(ascending=False)

        return self.stocks[code]
        

class StockAccount:
    '股票交易账户'

    def __init__(self, cash, max_credit = 0):
        self.max_credit = max_credit
        self.cash = cash
        self.credit = 0
        self.cost = 0
        self.market_value = cash

        self.max_value = cash
        self.max_back = 0
        self.max_lever = 0

        self.long_count = self.short_count = self.succeed = 0

        self.stocks = pf.DataFrame()
        self.records = []

    def status_info(self):
        print( self.long_count, self.short_count, self.succeed, 
            self.cash, self.credit, self.market_value, self.cost, 
            self.max_value, self.max_back, self.max_lever)

    def get_records(self):
        _records = pf.DataFrame(self.records, columns=['order_time', 'code', 'price', 
            'volume', 'amount', 'commision', 'total', 'total volume', 'total value',
            'cash', 'credit', 'market value', 'lever', 'back'])
        return _records

    def save_records(self, path, code):
        _records = self.get_records()
        _records.to_csv(path + '/' + code + '.records.csv')

    def Rechange(self, _cash):
        if self.credit > _cash:
            self.credit -= _cash
        elif self.credit > 0:
            self.cash += _cash - self.credit
            self.credit = 0
        else:
            self.cash += _cash

    def Cash(self, _capital):
        if( self.cash >= _capital ):
            self.cash -= _capital
        else:
            raise ValueError("Insufficient account balance")

    def UpdateValue(self, prices):
        self.market_value = self.cash - self.credit
        for code, row in self.stocks.iterrows():
            row['price'] = prices[code]
            row['market_value'] = row['price']*row['volume']
            self.market_value += row['market_value']

        lever = self.credit/self.market_value
        back_pump = 1 - self.market_value/self.max_value
        
        self.max_value = max(self.max_value, self.market_value)
        self.max_back  = max(self.max_back , back_pump)
        self.max_lever = max(self.max_lever, lever)


    def ProfitDaily(self):
        self.cash *= 1.00005
        self.credit *= 1.0003

    def Format(self, volume, price):
        volume = int(volume/100) * 100
        _value = price*volume
        absv = abs(_value)

        if absv * 0.001 < 5: # 手续费 千一
            _commision = 5
        else:
            _commision = absv * 0.001

        if volume < 0: # 印花税,单边收
            _commision += absv * 0.001
        _commision += absv * 0.00002 # 过户费
        _cost = _value + _commision
        return _cost, _commision, volume

    def Order(self, code, price, volume, order_time):
        _cost, _commision, volume = self.Format(volume, price)
        # print(order_time, code, price, volume, _cost, _commision, self.cash)

        if _cost < 0 and self.credit > 0:
            self.credit += _cost
            if self.credit < 0:
                self.cash -= self.credit
                self.credit = 0
        elif self.cash < _cost:
            if self.max_credit > 0 and self.credit + _cost - self.cash > self.max_credit:
                volume = (self.max_credit - self.credit + self.cash) / price
                _cost, _commision, volume = self.Format(volume, price)
            self.credit += _cost - self.cash
            self.cash = 0
        else:
            self.cash -= _cost
            
        self.cost += _commision
        order_time = num2date(order_time).strftime('%Y%m%d')

        if  code in self.stocks.index:
            if( self.stocks.loc[code]['volume'] + volume < 0 ):
                raise ValueError("Don't naked short sale.")

            _row = self.stocks.loc[code]
            _volume = _row.volume + volume
            if _volume == 0:
                _cost_price = _row.cost_price
                if _row.volume*_row.cost_price + _cost < 0: 
                    self.succeed += 1
            else:
                _cost_price = (_row.volume*_row.cost_price + _cost) / _volume
            mkt_value = _volume*price
            # print(self.cash, self.credit, _volume, _commision + _value, price, _cost_price, _volume*price, order_time)
            self.stocks.loc[code] = [_volume, price, _cost_price, mkt_value, order_time]

        else:
            if( volume <= 0 ):
                raise ValueError("Don't naked short sale.")
            _cost_price = _cost / volume
            _volume = volume
            mkt_value = volume*price
            _row = {'volume': [volume], 'price': [price], 'cost_price': [_cost_price], 
                'market_value': [mkt_value], 'order_time': [order_time]}
            _index = [code]
            # print(self.cash, self.credit, volume, _commision + _value, price, _cost_price, volume*price, order_time)
            self.stocks = self.stocks.append(pf.DataFrame(_row, _index))

        if volume < 0:
            self.short_count+= 1
        else:
            self.long_count += 1

        self.market_value = self.cash - self.credit + mkt_value
        lever = self.credit/self.market_value
        back_pump = 1 - self.market_value/self.max_value

        self.max_value = max(self.max_value, self.market_value)
        self.max_back  = max(self.max_back , back_pump)
        self.max_lever = max(self.max_lever, lever)

        _record = (order_time, code, price, volume, volume*price, _commision, _cost, 
            _volume, mkt_value, self.cash, self.credit, self.market_value, lever, back_pump)
        self.records.append(_record)
        # print(self.stocks)

class MovingAverage:
    '股票的移动平均线'

    def __init__(self, _prices):
        self.ma_indexs = {}
        self.prices = np.asarray(_prices)
        # self.moving_average(self.prices, _n)

    def moving_average(self, n):
        mas = []

        if n in self.ma_indexs:
            return self.ma_indexs[n]

        elif n == 1:
            mas.append(self.prices[0])
            for i in range(1, len(self.prices)):
                mas.append(self.prices[i-1])

        elif n == 2:
            mas.append(self.prices[0])
            mas.append(self.prices[0])
            for i in range(2, len(self.prices)):
                mas.append((self.prices[i-1] + self.prices[i-2])/2)

        else: # if n not in self.ma_indexs:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.ma_indexs:
                self.moving_average(m1)
                # self.ma_indexs[m1] = self.moving_average(m1)
            hs1 = self.ma_indexs[m1]

            if m2 not in self.ma_indexs:
                self.moving_average(m2)
                # self.ma_indexs[m2] = self.moving_average(m2)
            hs2 = self.ma_indexs[m2]

            for i in range(0, m2):
                mas.append(hs2[i])
            for i in range(m2, len(self.prices)):
                mas.append((hs2[i]*m2 + hs1[i-m2]*m1)/n)
        
        self.ma_indexs[n] = mas
        return self.ma_indexs[n]


# def parse_stock_data(stock_data):
#     data_list = []
#     ave_price = []
#     volumes = []

#     for rnum, row in stock_data.iterrows():
#         tscode, trade_date, close, open, high, low = row[0:6]
#         vol,amount = row[9:11]
#         _date = dt.datetime.strptime(trade_date, '%Y%m%d')
#         timenum = date2num(_date)

#         datas = (timenum, open, high, low, close)
#         data_list.append(datas)
#         ave_price.append( (high+low)/2 )
#         volumes.append(vol)

#     data_table = np.transpose( data_list )
#     dates = data_table[0]
#     return dates, data_list, ave_price, volumes
