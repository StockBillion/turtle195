#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np
from matplotlib.pylab import date2num, num2date
import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas as pf
from download import StockDataSet


def moving_average(x, n, type='simple'): 
    x = np.asarray(x) 

    if type == 'simple': 
        weights = np.ones(n) 
    else: 
        weights = np.exp(np.linspace(-1., 0., n)) 

    weights /= weights.sum() 
    a = np.convolve(x, weights, mode='full')[:len(x)] 
    a[:n] = a[n] 
    
    return a

def highest_price(x, n):
    x = np.asarray(x) 
    hs = []
    hs.append(x[0])

    for i in range(1, len(x)):
        h = x[i-1]
        start = max(0, i-n)
        for j in range(start, i):
            h = max(h, x[j])
        hs.append(h)

    return hs

def lowest_price(x, n):
    x = np.asarray(x) 
    ls = []
    ls.append(x[0])

    for i in range(1, len(x)):
        l = x[i-1]
        start = max(0, i-n)
        for j in range(start, i):
            l = min(l, x[j])
        ls.append(l)

    return ls

class StockAccount:
    '股票交易账户'
    market_value = 0
    cash = 0
    cost = 0
    stocks = pf.DataFrame()

    def __init__(self, cash):
        self.cash = cash

    def prt(self):
        print( "total balance = " , (self.market_value + self.cash), \
            "\nmarket value = " , self.market_value, "\ncapital = " , self.cash )

    def Rechange(self, _cash):
        self.cash += _cash

    def Cash(self, _capital):
        if( self.cash >= _capital ):
            self.cash -= _capital
        else:
            raise ValueError("Insufficient account balance")

    def UpdateValue(self, prices):
        self.market_value = self.cash
        # print(prices)
        for code, row in self.stocks.iterrows():
            row['price'] = prices[code]
            row['market_value'] = row['price']*row['volume']
            self.market_value += row['market_value']
            # print(prices[code])
            # print(code)
            # print(row)

    def Order(self, code, price, volume, order_time):
        # if order_time is float:
        order_time = num2date(order_time).strftime('%Y%m%d')
        _value = price*volume
        # if( self.cash - _value < 0 ):
        #     raise ValueError("not sufficient funds.")
        self.cash -= _value
        # print('order_time type', type(order_time))

        absv = abs(_value)
        if absv * 0.001 < 5:
            _cost = 5
        else:
            _cost = absv * 0.001

        if volume < 0:
            _cost += absv * 0.001
        _cost += absv * 0.00002
        self.cost += _cost

        if  code in self.stocks.index : 
            if( self.stocks.loc[code]['volume'] + volume < 0 ):
                raise ValueError("Don't naked short sale.")
            _row = self.stocks.loc[code]
            _volume = _row.volume + volume
            if _volume == 0:
                _cost = _row.cost
            else:
                _cost = (_row.volume*_row.cost + _cost + _value) / _volume
            # _cost = price*volune + _row.volume*_row.cost
            self.stocks.loc[code] = [_volume, price, _volume*price, _cost, order_time]

        else:
            if( volume <= 0 ):
                raise ValueError("Don't naked short sale.")
            _cost = (_cost + _value) / volume
            _row = {'volume': [volume], 'price': [price], 'market_value': [_value], 'cost': [_cost], 'order_time': [order_time]}
            _index = [code]
            self.stocks = self.stocks.append(pf.DataFrame(_row, _index))

        print(self.stocks)
        print(self.cash, self.market_value)

def moving_average_test(account, code, stock_data, stype = 'stock'):

    _date = datetime.datetime.strptime('20080101', '%Y%m%d')
    start_date = date2num(_date)

    data_list = []
    ave_price = []
    volumes = []
    market_values = []

    for rnum, row in stock_data.iterrows():
        tscode, trade_date, open, high, low, close = row[0:6]
        vol,amount = row[9:11]
        _date = datetime.datetime.strptime(trade_date, '%Y%m%d')
        timenum = date2num(_date)

        datas = (timenum, open, high, low, close)
        data_list.append(datas)
        ave_price.append( (high+low)/2 )
        volumes.append(vol)

    m120 = moving_average(ave_price, 120)
    m020 = moving_average(ave_price,  20)

    up120 = False
    up020 = False
    long_state = False
    need_long = False
    cash_unit = 0
    long_price = 0

    for n in range(0, 120):
        _date, _open, _high, _low, _close = data_list[n][0:5]
        if stype == 'index':
            _open = _open/1000
            _close/= 1000
        account.UpdateValue({code: _close})
        market_values.append(account.market_value *.025)

    for n in range(120, len(stock_data)):
        _date, _open, _high, _low, _close = data_list[n][0:5]
        # order_time = num2date(order_time).strftime('%Y%m%d')

        if stype == 'index':
            _open = _open/1000
            _close/= 1000

        if _date < start_date:
            account.UpdateValue({code: _close})
            market_values.append(account.market_value *.025)
            continue

        if need_long:
            need_long = False
            if account.cash >= -cash_unit*2:
                volume = cash_unit / _open
                volume = int(volume/100) * 100
                account.Order(code, _open, volume, _date)

        # if up120 and up020 and (not long_state):
        #     volume = account.cash / _open
        #     volume = int(volume/100) * 100
        #     long_state = account.Order(code, _open, volume, _date)
            
        if (not up020) and long_state:
            volume = account.stocks.at[code, 'volume']
            account.Order(code, _open, -volume, _date)
            long_state = False
            # long_state = not account.Order(code, _open, -volume, _date)

        if m120[n] < data_list[n][2]:
            up120 = True
        else:
            up120 = False

        if m020[n] > data_list[n][3]:
            up020 = False
        else:
            up020 = True

        if up120 and up020 and (not long_state):
            long_state = True
            cash_unit = account.cash/3
            long_price = _close
            # need_long = True

        if long_state and _close >= long_price:
            need_long = True
            long_price = _close * 1.02
            
        # if (not up020) and long_state:
        #     long_state = False

        account.UpdateValue({code: _close})
        market_values.append(account.market_value *.025)

        # _date = data_list[n][0]
        # _open = data_list[n][1]
        # print('up120', up120, 'up020', up020, 'long_state', long_state)

            # print('long price', _open, 'volume', volume, 'date', _date)
            # long_state = True

            # print('short price', _open, 'volume', volume, 'date', _date)
            # long_state = False

    # account.UpdateValue({code: 0})
    # print(account.stocks)
    # return

    fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)
    # fig.subplots_adjust(bottom=0.2)

    ax1.xaxis_date()
    ax1.set_title(code)
    ax1.set_ylabel("price")

    plt.xticks(rotation=45)
    plt.yticks()

    mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')

    data_table = np.transpose( data_list )
    dates = data_table[0]
    ax1.plot(dates, m120, color='g', lw=2, label='MA (120)')
    ax1.plot(dates, m020, color='b', lw=2, label='MA (20)')
    ax1.plot(dates, market_values, color='r', lw=2, label='MV')

    # print(market_value)
    # print(m020)

    ax2.bar(dates, volumes, width=0.75)
    ax2.set_ylabel('Volume')

    plt.xlabel("date")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    dataset = StockDataSet()
    account = StockAccount(100000)

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
        startdate = str(ARGS.start_date)
    if ARGS.end_date:
        enddate = str(ARGS.end_date)
    if ARGS.data_type:
        stype = str(ARGS.data_type)
    if ARGS.filename:
        stock_codes = ARGS.filename

    for code in stock_codes:
        dataset.load(code, startdate, enddate, stype)
        moving_average_test(account, code, dataset.stocks[code], stype)
        print(account.cash)



        # up120 = m120[n] < data_list[n][2] ? True : False
        # print(m120[n], m020[n], data_list[n][2], data_list[n][3])

    # state = 0
    # doing = 0

    # for n in range(121, len(stock_data)):
    #     _date = data_list[n][0]
    #     _open = data_list[n][1]
    #     if stype == 'index':
    #         _open = _open/100

    #     if doing == 1:
    #         volume = account.cash / _open
    #         volume = int(volume/100) * 100
    #         account.Order(code, _open, volume, _date)
    #         state = 1
    #         doing = 0
    #     elif doing == -1:
    #         volume = account.stocks.at[code, 'volume']
    #         # volume = account.stocks[code]['volume']
    #         account.Order(code, _open, -volume, _date)
    #         state = 0
    #         doing = 0

    #     if state == 0 and m120[n] < data_list[n][2]:
    #         doing = 1
    #     if state == 1 and m020[n] > data_list[n][3]:
    #         doing = -1
