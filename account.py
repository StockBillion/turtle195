#!/usr/bin/env python
#-*- coding: utf8 -*-
import numpy as np
from matplotlib.pylab import date2num, num2date
import pandas as pf

class StockAccount:
    '股票交易账户'

    stocks = pf.DataFrame()
    market_value = 0
    cash = 0
    cost = 0
    long_count = 0
    short_count= 0
    succeed = 0
    records = []


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
        for code, row in self.stocks.iterrows():
            row['price'] = prices[code]
            row['market_value'] = row['price']*row['volume']
            self.market_value += row['market_value']

    def Order(self, code, price, volume, order_time):
        # print(code, price, volume, price*volume, self.cash)
        _value = price*volume
        # if( self.cash < _value ):
        #     raise ValueError("not sufficient funds.")

        self.cash -= _value
        order_time = num2date(order_time).strftime('%Y%m%d')

        absv = abs(_value)
        if absv * 0.001 < 5: # 手续费 千一
            _commision = 5
        else:
            _commision = absv * 0.001

        if volume < 0: # 印花税,单边收
            _commision += absv * 0.001
        _commision += absv * 0.00002 # 过户费
        self.cost += _commision


        if  code in self.stocks.index:
            if( self.stocks.loc[code]['volume'] + volume < 0 ):
                raise ValueError("Don't naked short sale.")

            _row = self.stocks.loc[code]
            _volume = _row.volume + volume
            if _volume == 0:
                _cost_price = _row.cost_price
                if _row.volume*_row.cost_price + _commision + _value < 0: 
                    self.succeed += 1
            else:
                _cost_price = (_row.volume*_row.cost_price + _commision + _value) / _volume
            _value = _volume*price
            self.stocks.loc[code] = [_volume, price, _value, _cost_price, order_time]

        else:
            if( volume <= 0 ):
                raise ValueError("Don't naked short sale.")
            _cost_price = (_commision + _value) / volume
            _row = {'volume': [volume], 'price': [price], 'market_value': [_value], 
                'cost_price': [_cost_price], 'order_time': [order_time]}
            _index = [code]
            self.stocks = self.stocks.append(pf.DataFrame(_row, _index))

        if volume < 0:

            self.short_count+= 1
        else:
            self.long_count += 1

        _record = (order_time, volume, price, volume*price, _commision, (volume*price + _commision), 
            self.cash, self.cash + _value)
        self.records.append(_record)

        # print(self.stocks)
        # print(self.cash, self.market_value, self.stocks.loc[code, 'volume'], 
        #     self.stocks.loc[code, 'price'], self.stocks.loc[code, 'order_time'])
