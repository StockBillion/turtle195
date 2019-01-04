#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np
from matplotlib.pylab import date2num, num2date
import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas as pf

from stockdata import StockDataSet, parse_stock_data
from account import StockAccount

class MovingAverage:
    '股票的移动平均线'

    def __init__(self, _prices, _n):
        self.ma_indexs = {}
        self.prices = np.asarray(_prices)
        self._moving_average(self.prices, _n)

    def _moving_average(self, prices, n):
        mas = []

        if n == 1:
            mas.append(prices[0])
            for i in range(1, len(prices)):
                mas.append(prices[i-1])

        elif n == 2:
            mas.append(prices[0])
            mas.append(prices[0])
            for i in range(2, len(prices)):
                mas.append((prices[i-1] + prices[i-2])/2)

        else:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.ma_indexs:
                self.ma_indexs[m1] = self._moving_average(prices, m1)
            if m2 not in self.ma_indexs:
                self.ma_indexs[m2] = self._moving_average(prices, m2)

            hs1 = self.ma_indexs[m1]
            hs2 = self.ma_indexs[m2]
            for i in range(0, m2):
                mas.append(hs2[i])
            for i in range(m2, len(prices)):
                mas.append((hs2[i]*m2 + hs1[i-m2]*m1)/n)

        self.ma_indexs[n] = mas
        return mas


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

def moving_average_test(account, code, stock_data, stype = 'stock'):

    _date = datetime.datetime.strptime('20080101', '%Y%m%d')
    start_date = date2num(_date)

    dates, data_list, ave_price, volumes = parse_stock_data(stock_data)
    m120 = moving_average(ave_price, 120)
    m040 = moving_average(ave_price,  40)

    up120 = False
    up040 = False
    long_state = False
    need_long = False
    long_price = 0
    long_count = 0
    cash_unit = 0
    market_values = []
    stock_volumes = []

    for n in range(0, len(stock_data)):
        _date, _open, _high, _low, _close = data_list[n][0:5]
        # order_time = num2date(order_time).strftime('%Y%m%d')

        if stype == 'index':
            _open /= 1000
            _close/= 1000

        if _date < start_date:
            account.UpdateValue({code: _close})
            market_values.append(account.market_value *.025)
            stock_volumes.append(0)
            continue

        if need_long and long_count < 120:
            volume = cash_unit / _open
            volume = int(volume/100) * 100
            account.Order(code, _open, volume, _date)
            long_count = long_count+1
            need_long = False
            
        if (not up040 or not up120 ) and long_state:
            volume = account.stocks.at[code, 'volume']
            account.Order(code, _open, -volume, _date)
            long_state = False
            long_price = 0
            long_count = 0

        if m120[n] < data_list[n][2]:
            up120 = True
        else:
            up120 = False

        if m040[n] > data_list[n][3]:
            up040 = False
        else:
            up040 = True

        if up120 and up040 and (not long_state):
            long_state = True
            cash_unit = account.cash
            need_long = True
            long_price = _close
        if long_state and _close >= long_price:
            need_long = True
            long_price = _close * 1.05
            

        account.UpdateValue({code: _close})
        market_values.append(account.market_value *.025)
        if  code in account.stocks.index:
            volume = account.stocks.at[code, 'volume']
        else:
            volume = 0
        stock_volumes.append(volume)

    fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)

    ax1.xaxis_date()
    ax1.set_title(code)
    ax1.set_ylabel("price")

    plt.xticks(rotation=45)
    plt.yticks()

    mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')
    ax1.plot(dates, m120, color='y', lw=2, label='MA (120)')
    ax1.plot(dates, m040, color='b', lw=2, label='MA (40)')
    ax1.plot(dates, market_values, color='r', lw=2, label='MV')

    # ax2.bar(dates, volumes, width=0.75)
    # ax2.bar(dates, volumes, color='b')
    # ax2.bar(dates, stock_volumes, color='r')
    ax2.plot(dates, stock_volumes, color='r', lw=2, label='volumes')
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
        print(account.cash, account.market_value)



        # if need_long:
        #     need_long = False
        #     if long_count < 6: # account.cash >= -cash_unit*2: #
        #         # print(account.cash, cash_unit, -cash_unit*3)
        #         volume = cash_unit / _open
        #         volume = int(volume/100) * 100
        #         account.Order(code, _open, volume, _date)
        #         long_count = long_count+1

        # if up120 and up020 and (not long_state):
        #     volume = account.cash / _open
        #     volume = int(volume/100) * 100
        #     long_state = account.Order(code, _open, volume, _date)
            
    # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)
    # fig.subplots_adjust(bottom=0.2)

    # long_price = 0

    # for n in range(0, 120):
    #     _date, _open, _high, _low, _close = data_list[n][0:5]
    #     if stype == 'index':
    #         _open = _open/1000
    #         _close/= 1000
    #     account.UpdateValue({code: _close})
    #     market_values.append(account.market_value *.025)
    #     stock_volumes.append(0)

    # data_table = np.transpose( data_list )
    # dates = data_table[0]

    # data_list = []
    # ave_price = []
    # volumes = []

    # for rnum, row in stock_data.iterrows():
    #     tscode, trade_date, open, high, low, close = row[0:6]
    #     vol,amount = row[9:11]
    #     _date = datetime.datetime.strptime(trade_date, '%Y%m%d')
    #     timenum = date2num(_date)

    #     datas = (timenum, open, high, low, close)
    #     data_list.append(datas)
    #     ave_price.append( (high+low)/2 )
    #     volumes.append(vol)

        # if (not up020) and long_state:
        #     long_state = False

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

    # print(market_value)
    # print(m020)

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
