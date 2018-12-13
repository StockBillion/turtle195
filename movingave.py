#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np
from matplotlib.pylab import date2num
import datetime
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

    def Order(self, code, price, volume, order_time):
        _value = price*volume
        if( self.cash - _value < 0 ):
            raise ValueError("not sufficient funds.")
        self.cash -= _value

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

def moving_average_test(account, code, stock_data):
    data_list = []
    ave_price = []
    volumes = []

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

    # print(m020)
    # print(data_list[1][0])

    state = 0
    doing = 0

    for n in range(121, len(stock_data)):
        if doing == 1:
            volume = account.cash / data_list[n][1]
            volume = int(volume/100) * 100
            account.Order(code, data_list[n][1], volume, data_list[n][0])
            state = 1
            doing = 0
        elif doing == -1:
            volume = account.stocks.at[code, 'volume']
            # volume = account.stocks[code]['volume']
            account.Order(code, data_list[n][1], -volume, data_list[n][0])
            state = 0
            doing = 0

        if state == 0 and m120[n] < data_list[n][2]:
            doing = 1
        if state == 1 and m020[n] > data_list[n][2]:
            doing = -1


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
        moving_average_test(account, code, dataset.stocks[code])
        print(account.cash)


