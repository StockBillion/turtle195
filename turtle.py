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
    # ma_indexs = {}
    # prices = []

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
                # _ma = hs2[i]*m2 + hs1[i-m2]*m1
                # mas.append(_ma/n)

        self.ma_indexs[n] = mas
        return mas


class TurTleIndex:
    '海龟指标'

    # high_indexs = {}
    # low_indexs = {}
    # high = []
    # low = []

    def __init__(self, highs, lows, hn, ln):
        self.high_indexs = {}
        self.low_indexs = {}

        self.high = np.asarray(highs)
        self.low  = np.asarray(lows )

        self._highest_price(self.high, hn)
        self._lowest_price (self.low,  ln)

    def _highest_price(self, x, n):
        hs = []

        if n == 1:
            hs.append(x[0])
            for i in range(1, len(x)):
                hs.append(x[i-1])

        elif n == 2:
            hs.append(x[0])
            hs.append(x[0])
            for i in range(2, len(x)):
                hs.append(max(x[i-1], x[i-2]))

        else:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.high_indexs:
                self.high_indexs[m1] = self._highest_price(x, m1)
            if m2 not in self.high_indexs:
                self.high_indexs[m2] = self._highest_price(x, m2)

            hs1 = self.high_indexs[m1]
            hs2 = self.high_indexs[m2]
            for i in range(0, m2):
                hs.append(hs2[i])
            for i in range(m2, len(x)):
                hs.append(max(hs2[i], hs1[i-m2]))

        self.high_indexs[n] = hs
        return hs

    def highest_price(self, x, n):
        return self._highest_price(np.asarray(x), n)

    def _lowest_price(self, x, n):
        ls = []

        if n == 1:
            ls.append(x[0])
            for i in range(1, len(x)):
                ls.append(x[i-1])

        elif n == 2:
            ls.append(x[0])
            ls.append(x[0])
            for i in range(2, len(x)):
                ls.append(min(x[i-1], x[i-2]))

        else:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.low_indexs:
                self.low_indexs[m1] = self._lowest_price(x, m1)
            if m2 not in self.low_indexs:
                self.low_indexs[m2] = self._lowest_price(x, m2)

            ls1 = self.low_indexs[m1]
            ls2 = self.low_indexs[m2]
            for i in range(0, m2):
                ls.append(ls2[i])
            for i in range(m2, len(x)):
                ls.append(min(ls2[i], ls1[i-m2]))

        self.low_indexs[n] = ls
        return ls

    def lowest_price(self, x, n):
        return self._lowest_price(np.asarray(x), n)


def list_multi(x):
    x *= 0.01
    return x

def turtle_test(account, code, stock_data, stype = 'stock', long_cycle = 20, short_cycle = 10):
    _date = datetime.datetime.strptime('20080101', '%Y%m%d')
    start_date = date2num(_date)
    _date = datetime.datetime.strptime('20190101', '%Y%m%d')
    end_date = date2num(_date)

    dates, data_list, ave_price, volumes = parse_stock_data(stock_data)
    data_table = np.transpose( data_list )

    if stype == 'index':
        ave_price = list(map(list_multi, ave_price))
        data_table[1] = list(map(list_multi, data_table[1]))
        data_table[2] = list(map(list_multi, data_table[2]))
        data_table[3] = list(map(list_multi, data_table[3]))
        data_table[4] = list(map(list_multi, data_table[4]))
        data_list = np.transpose( data_table )


    avema = MovingAverage(ave_price, 240)
    avma240 = avema.ma_indexs[240]
    wavema = MovingAverage(data_table[2] - data_table[3], 20)
    wvma20 = wavema.ma_indexs[20]

    turtle = TurTleIndex(data_table[2], data_table[3], long_cycle, short_cycle)
    h55 = turtle.high_indexs[long_cycle]
    l20 = turtle.low_indexs[short_cycle]

    long_price = 0
    long_count = 0
    cash_unit = 0
    market_values = []
    stock_volumes = []

    for n in range(0, len(stock_data)):
        _date, _open, _high, _low, _close = data_list[n][0:5]

        if _date < start_date or _date > end_date:
            account.UpdateValue({code: _close})
            market_values.append(account.market_value *.000025)
            stock_volumes.append(0)
            continue

        # if long_count > 0 and data_list[n][3] < l20[n]:
        #     volume = account.stocks.at[code, 'volume']
        #     account.Order(code, _open, -volume, _date)
        #     long_count = 0

        if long_count > 0 and (data_list[n][3] < l20[n] or data_list[n][3] < long_price - wvma20[n]*3):
            volume = account.stocks.at[code, 'volume']
            account.Order(code, _open, -volume, _date)
            long_count = 0

        if h55[n] < data_list[n][2] and not long_count:
            # print(account.cash, h55[n], l20[n], wvma20[n])
            # print(_open, _high, _low, _close)

            # volume = account.cash * .005 / wvma20[n]
            # volume = int(volume/100) * 100
            # cash_unit = volume * h55[n]

            cash_unit = account.cash * .03 * h55[n] / wvma20[n]
            if _open < h55[n]:
                long_price = h55[n]
            else:
                long_price = _open

            volume = cash_unit / long_price
            volume = int(volume/100) * 100
            account.Order(code, long_price, volume, _date)
            long_price = long_price + wvma20[n]
            long_count = long_count+1

        if long_count > 0 and data_list[n][2] > long_price and long_count < 4:
            if _open > long_price:
                long_price = _open
            
            volume = cash_unit / long_price
            volume = int(volume/100) * 100
            account.Order(code, long_price, volume, _date)
            long_price = long_price + wvma20[n]
            long_count = long_count+1

        account.UpdateValue({code: _close})
        market_values.append(account.market_value *.000025)
        if  code in account.stocks.index:
            volume = account.stocks.at[code, 'volume']
        else:
            volume = 0
        stock_volumes.append(volume)


    print( pf.DataFrame(account.records, columns=['order_time', 'volume', 'price', 
        'amount', 'commision', 'total', 'cash', 'market value']) )
    print( account.long_count, account.short_count, account.succeed)

    fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)

    ax1.xaxis_date()
    ax1.set_title(code)
    ax1.set_ylabel("price")

    plt.xticks(rotation=45)
    plt.yticks()

    mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')
    ax1.plot(dates, h55, color='y', lw=2, label='high (long_cycle)')
    ax1.plot(dates, l20, color='b', lw=2, label='low (short_cycle)')
    ax1.plot(dates, avma240, color='g', lw=2, label='MA (240)')
    ax1.plot(dates, market_values, color='r', lw=2, label='MV')

    # ax2.bar(dates, volumes, width=0.75)
    ax2.plot(dates, wvma20, color='r', lw=2, label='wave')
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
    time_unit = 'daily'

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument('filename', default=['601857.sh'], nargs='*')
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")
    parser.add_argument("-t", "--data_type", help="data type")
    parser.add_argument("-u", "--time_unit", help="time unit")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = str(ARGS.start_date)
    if ARGS.end_date:
        enddate = str(ARGS.end_date)
    if ARGS.data_type:
        stype = str(ARGS.data_type)
    if ARGS.filename:
        stock_codes = ARGS.filename
    if ARGS.time_unit:
        time_unit = ARGS.time_unit

    for code in stock_codes:
        dataset.load(code, startdate, enddate, stype, time_unit)
        turtle_test(account, code, dataset.stocks[code], stype, 55, 20)
        print(account.cash, account.market_value)



    # print(data_list[20])
    # print(data_table[0][20:25])
    # print(data_table[1][20:25])
    # print(data_table[2][20:25])
    # print(data_table[3][20:25])
    # print(data_table[4][20:25])


    # print(data_list[20])
    # print(data_table[0][20:25])
    # print(data_table[1][20:25])
    # print(data_table[2][20:25])
    # print(data_table[3][20:25])
    # print(data_table[4][20:25])

    # h55 = turtle.highest_price(data_table[2], 55)
    # l20 = turtle.lowest_price (data_table[3], 20)

    # l20 = lowest_price(data_table[3], 20)

    # h55 = highest_price(data_table[2], 55)
    # h20 = highest_price(data_table[2], 20)

    # print(ave_price[250: 270])
    # print(avema.ma_indexs[1][250: 270])
    # print(avema.ma_indexs[2][250: 270])
    # print(avema.ma_indexs[3][250: 270])
    # print(avema.ma_indexs[5][250: 270])
    # print(avma240[250: 270])

# hs_set = {}
# def highest_price_core(x, n):
#     hs = []

#     if n == 1:
#         hs.append(x[0])
#         for i in range(1, len(x)):
#             hs.append(x[i-1])

#     elif n == 2:
#         hs.append(x[0])
#         hs.append(x[0])
#         for i in range(2, len(x)):
#             hs.append(max(x[i-1], x[i-2]))

#     else:
#         m1 = int(n/2)
#         m2 = n - m1

#         if m1 not in hs:
#             hs_set[m1] = highest_price_core(x, m1)
#         if m2 not in hs:
#             hs_set[m2] = highest_price_core(x, m2)

#         hs1 = hs_set[m1]
#         hs2 = hs_set[m2]
#         for i in range(0, m2):
#             hs.append(hs2[i])
#         for i in range(m2, len(x)):
#             hs.append(max(hs2[i], hs1[i-m2]))

#     return hs

# def highest_price(x, n):
#     return highest_price_core(np.asarray(x), n)

#     # x = np.asarray(x) 
#     # hs = []
#     # hs.append(x[0])

#     # for i in range(1, len(x)):
#     #     h = x[i-1]
#     #     start = max(0, i-n)
#     #     for j in range(start, i):
#     #         h = max(h, x[j])
#     #     hs.append(h)

#     # return hs

# def lowest_price(x, n):
#     x = np.asarray(x) 
#     ls = []
#     ls.append(x[0])

#     for i in range(1, len(x)):
#         l = x[i-1]
#         start = max(0, i-n)
#         for j in range(start, i):
#             l = min(l, x[j])
#         ls.append(l)

#     return ls
