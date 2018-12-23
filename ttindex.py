#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np, pandas as pd
import matplotlib.pyplot as plt, mpl_finance as mpf
# from enum import Enum
from stockdata import StockDataSet, parse_stock_data
from account import StockAccount


index_code = '000300.sh'
stock_codes = ['601398.sh', '601988.sh', '601628.sh', '600028.sh', '600036.sh', '601318.sh', 
	'601328.sh', '600000.sh', '601998.sh', '601166.sh', '600030.sh', '600016.sh', 
	'600519.sh', '600019.sh', '600050.sh', '600104.sh', '601006.sh', '600018.sh', 
	'000858.sz', '601111.sh', '000002.sz', '600900.sh', '601601.sh', '601991.sh' ]

# # https://tushare.pro/
# ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
# pro = ts.pro_api()

# df = pro.index_weight(index_code='399300.SZ', start_date='20180901', end_date='20180930')
# print(df)



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


# class StrongIndex:
#     '强弱指标'
#     def __init__(self)

class TurTleIndex:
    '海龟指标'

    def __init__(self, data_list, long_period, short_period, append_multiple, loss_multiple):
        data_table = np.transpose( data_list )

        self.data = {}
        self.strong = {}
        self.wave = {}

        self.high_prices = {}
        self.high_locats = {}
        self.low_prices = {}
        self.low_locats = {}

        self.data['date'] = data_table[0]
        self.data['open'] = data_table[1]
        self.data['high'] = data_table[2]
        self.data['low' ] = data_table[3]
        self.data['close'] = data_table[4]

        self._highest_price(self.data['high'], long_period)
        self._highest_price(self.data['high'], short_period)
        self._lowest_price (self.data['low' ], long_period)
        self._lowest_price (self.data['low' ], short_period)

        price_wave = self.data['high'] - self.data['low']
        wavema = MovingAverage(price_wave)
        self.wave[1] = price_wave
        self.wave[long_period ] = wavema.moving_average(long_period)
        self.wave[short_period] = wavema.moving_average(short_period)

        self.trade(long_period, short_period, append_multiple, loss_multiple)
        self.strong_index(5)
        self.strong_index(20)
        self.strong_index(60)

        self.data['lh_price'] = self.high_prices[10]
        # self.data['lh_locat'] = self.high_locats[10]
        self.data['ll_price'] = self.low_prices[10]
        # self.data['ll_locat'] = self.low_locats[10]

        print( pd.DataFrame(self.strong)[220: 250] )
        print( pd.DataFrame(self.data)[220: 250] )

        # print( pd.DataFrame(self.wave)[55: 85] )
        # print( pd.DataFrame(self.high_prices)[55: 85] )
        # print( pd.DataFrame(self.high_prices)[55: 85] )

        # self.data['long_wave'] = self.wave[long_period ]
        # self.data['short_wave'] = self.wave[short_period]

        # self.data['lh_price'] = self.high_prices[long_period]
        # self.data['ll_price'] = self.low_prices[long_period]
        # self.data['sh_price'] = self.high_prices[short_period]
        # self.data['sl_price'] = self.low_prices[short_period]

        # self.data['lh_locat'] = self.high_locats[long_period]
        # self.data['ll_locat'] = self.low_locats[long_period]
        # self.data['sh_locat'] = self.high_locats[short_period]
        # self.data['sl_locat'] = self.low_locats[short_period]

        # self.data['long_wave'] = wavema.ma_indexs[long_period]
        # self.data['short_wave'] = wavema.ma_indexs[short_period]

        # print( pd.DataFrame(self.data)[55: 85] )
        # self.high = np.asarray(highs)
        # self.low  = np.asarray(lows )

    def strong_index(self, period):
        _strong = []

        close = self.data['close']
        high = self.data['high']
        low  = self.data['low' ]

        self._highest_price(high, period)
        self._lowest_price (low , period)
        self._highest_price(high, period*3)
        self._lowest_price (low , period*3)

        HP1 = self.high_prices[period]
        LP1 = self.low_prices [period]
        HP3 = self.high_prices[period*3]
        LP3 = self.low_prices [period*3]

        # HP = self.high_prices[period]
        # LP = self.low_prices [period]
        # HL = self.high_locats[period]
        # LL = self.low_locats [period]

        _strong.append(0)
        for i in range(1, len(high)):
            s = (HP1[i] - LP3[i])/LP3[i] + (LP1[i] - HP3[i])/HP3[i]
            # s = (close[i] - LP3[i])/LP3[i]
            # s = (high[i] - LP[i])/LP[i] + (low[i] - HP[i])/HP[i]
            # s = (close[i] - LP[i]) / (i - LL[i]) + (close[i] - HP[i]) / (i - HL[i])
            _strong.append(s*100)

        self.strong[period] = _strong

        # self._highest_price(self.data['high'], 40)
        # self._highest_price(self.data['high'], 120)
        # self._lowest_price (self.data['low' ], 40)
        # self._lowest_price (self.data['low' ], 120)

        # strong10 = []
        # strong10 

    def trade(self, long_period, short_period, append_multiple, loss_multiple):
        state = []
        key_prices = []
        long_count = 0
        keyprice = 0

        LH = self.high_prices[long_period]
        SL = self.low_prices[short_period]
        SN = self.wave[short_period]

        open = self.data['open']
        high = self.data['high']
        low  = self.data['low' ]

        for i in range(0, long_period):
            state.append(long_count)
            key_prices.append(0)

        for i in range(long_period, len(high)):
            stop_price = max(SL[i], keyprice - SN[i] * loss_multiple)
            # append_price = max(lh[i], keyprice + N[i] * append_multiple)
            if long_count > 0:
                append_price = keyprice + SN[i] * append_multiple
            else:
                append_price = LH[i]

            # print(self.data['date'][i], high[i], low[i], sl[i], lh[i], N[i], 
            #     stop_price, append_price, long_count, keyprice)

            if high[i] > append_price:
                long_count += 1
                if open[i] > append_price:
                    keyprice = open[i]
                else:
                    keyprice = append_price

            if long_count > 0 and low[i] < stop_price:
                long_count = 0
                if open[i] < stop_price:
                    keyprice = open[i]
                else:
                    keyprice = stop_price

            state.append(long_count)
            key_prices.append(keyprice)

        self.data['state'] = state
        self.data['key_prices'] = key_prices

    def _highest_price(self, x, n):
        ps = []
        ls = []

        if n == 1:
            ps.append(x[0])
            ls.append(0)

            for i in range(1, len(x)):
                ps.append(x[i-1])
                ls.append(i-1)

        elif n == 2:
            ps.append(x[0])
            ls.append(0)
            ps.append(x[0])
            ls.append(0)

            for i in range(2, len(x)):
                if x[i-1] > x[i-2]:
                    ps.append(x[i-1])
                    ls.append(i-1)
                else:
                    ps.append(x[i-2])
                    ls.append(i-2)

        else:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.high_prices:
                self._highest_price(x, m1)
            ps1 = self.high_prices[m1]
            ls1 = self.high_locats[m1]

            if m2 not in self.high_prices:
                self._highest_price(x, m2)
            ps2 = self.high_prices[m2]
            ls2 = self.high_locats[m2]

            for i in range(0, m2):
                ps.append(ps2[i])
                ls.append(ls2[i])

            for i in range(m2, len(x)):
                if ps2[i] > ps1[i-m2]:
                    ps.append(ps2[i])
                    ls.append(ls2[i])
                else:
                    ps.append(ps1[i-m2])
                    ls.append(ls1[i-m2])

        self.high_prices[n] = ps
        self.high_locats[n] = ls

    def _lowest_price(self, x, n):
        ps = []
        ls = []

        if n == 1:
            ps.append(x[0])
            ls.append(0)

            for i in range(1, len(x)):
                ps.append(x[i-1])
                ls.append(i-1)

        elif n == 2:
            ps.append(x[0])
            ls.append(0)
            ps.append(x[0])
            ls.append(0)

            for i in range(2, len(x)):
                if x[i-1] < x[i-2]:
                    ps.append(x[i-1])
                    ls.append(i-1)
                else:
                    ps.append(x[i-2])
                    ls.append(i-2)

        else:
            m1 = int(n/2)
            m2 = n - m1

            if m1 not in self.low_prices:
                self._lowest_price(x, m1)
            ps1 = self.low_prices[m1]
            ls1 = self.low_locats[m1]

            if m2 not in self.low_prices:
                self._lowest_price(x, m2)
            ps2 = self.low_prices[m2]
            ls2 = self.low_locats[m2]

            for i in range(0, m2):
                ps.append(ps2[i])
                ls.append(ls2[i])

            for i in range(m2, len(x)):
                if ps2[i] < ps1[i-m2]:
                    ps.append(ps2[i])
                    ls.append(ls2[i])
                else:
                    ps.append(ps1[i-m2])
                    ls.append(ls1[i-m2])

        self.low_prices[n] = ps
        self.low_locats[n] = ls


## 计算指标
# def calc_ttindex(data_frame, long_cycle, short_cycle, append_multiple, loss_multiple):
#     dates, data_list, ave_price, volumes = parse_stock_data(data_frame)
#     turtle = TurTleIndex(data_list, long_cycle, short_cycle, append_multiple, loss_multiple)

    # data_table = np.transpose( data_list )
    # print( data_frame['high'][5] )

    # wavema = MovingAverage(data_table[2] - data_table[3], short_cycle)
    # wvma20 = wavema.ma_indexs[short_cycle]

    # turtle = TurTleIndex(data_table[2], data_table[3], long_cycle, short_cycle)
    # high_index = turtle.high_prices[long_cycle]
    # low_index = turtle.low_prices[short_cycle]

    # print(data_frame)
    # print(pf.DataFrame(turtle.high_prices))
    # print(pf.DataFrame(turtle.high_locats))
    # print(turtle.low_prices[short_cycle])
    # print(turtle.low_locats[short_cycle])


if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20150101'
    enddate = '20190101'

    long_cycle = 55
    short_cycle= 20
    stock_datas = {}

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = ARGS.start_date
    if ARGS.end_date:
        enddate = ARGS.end_date

## 准备数据
    index_data = dataset.load(index_code, startdate, enddate, 'index', 'daily')
    # for code in stock_codes:
    #     stock_datas[code] = dataset.load(code, startdate, enddate, 'stock', 'daily')

# ## 计算指标
    # calc_ttindex(index_data, long_cycle, short_cycle, 1, 2)
#     for code in stock_codes:
# 		calc_ttindex(stock_datas[code], long_cycle, short_cycle)


    dates, data_list, ave_price, volumes = parse_stock_data(index_data)
    turtle = TurTleIndex(data_list, long_cycle, short_cycle, 1, 2)

    h55 = turtle.high_prices[55]
    l20 = turtle.low_prices[20]
    # strong = turtle.strong[120]

    fig,[ax1,ax2] = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)

    ax1.xaxis_date()
    ax1.set_title(index_code)
    ax1.set_ylabel("price")

    plt.xticks(rotation=45)
    plt.yticks()
    plt.xlabel("date")


    mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')
    ax1.plot(dates, h55, color='y', lw=2, label='high (long_cycle)')
    ax1.plot(dates, l20, color='b', lw=2, label='low (short_cycle)')

    # ax1.plot(dates, avma240, color='g', lw=2, label='MA (240)')
    # ax1.plot(dates, market_values, color='r', lw=2, label='MV')

    # ax2.bar(dates, volumes, width=0.75)

    # ax2.plot(dates, stock_volumes, color='r', lw=2, label='volumes')

    ax2.plot(dates, turtle.strong[5], color='r', lw=2, label='wave')
    ax2.plot(dates, turtle.strong[20], color='g', lw=2, label='wave')
    ax2.plot(dates, turtle.strong[60], color='b', lw=2, label='wave')
    ax2.set_ylabel('Volume')

    plt.grid()
    # plt.savefig("./images/turtle2055.png")
    plt.show()


    # TTState = Enum('TTState', ('NONE', 'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'STOP_LOSS', 'STOP_PROFIT'))

    # dates, data_list, ave_price, volumes = parse_stock_data(index_data)
    # data_table = np.transpose( data_list )
    # wavema = MovingAverage(data_table[2] - data_table[3], short_cycle)
    # wvma20 = wavema.ma_indexs[short_cycle]

    # turtle = TurTleIndex(data_table[2], data_table[3], long_cycle, short_cycle)
    # h55 = turtle.high_indexs[long_cycle]
    # l20 = turtle.low_indexs[short_cycle]

    # for code in stock_codes:
    #     dates, data_list, ave_price, volumes = parse_stock_data(stock_datas[code])
    #     data_table = np.transpose( data_list )
    #     wavema = MovingAverage(data_table[2] - data_table[3], short_cycle)
    #     wvma20 = wavema.ma_indexs[short_cycle]

    #     turtle = TurTleIndex(data_table[2], data_table[3], long_cycle, short_cycle)
    #     h55 = turtle.high_indexs[long_cycle]
    #     l20 = turtle.low_indexs[short_cycle]



            # if high[i] > lh[i] and not long_count:
            #     long_count = 1
            #     if open[i] > stop_price:
            #         keyprice = open[i]
            #     else:
            #         keyprice = lh[i]
            # elif long_count and high[i] > append_price:
            #     long_count += 1
            #     if open[i] > append_price:
            #         keyprice = open[i]
            #     else:
            #         keyprice = append_price


    # def __init__(self, dates, highs, lows, long_period, short_period):
    #     self.data = {}

    #     self.high_prices = {}
    #     self.high_locats = {}
    #     self.low_prices = {}
    #     self.low_locats = {}

    #     self.high = np.asarray(highs)
    #     self.low  = np.asarray(lows )

    #     self._highest_price(self.high, long_period)
    #     self._highest_price(self.high, short_period)
    #     self._lowest_price (self.low,  long_period)
    #     self._lowest_price (self.low,  short_period)

    #     self.data['date'] = np.asarray(dates)
    #     self.data['high'] = np.asarray(highs)
    #     self.data['low '] = np.asarray(lows )
    #     self.data['low '] = np.asarray(lows )

# from movingave import MovingAverage

# from matplotlib.pylab import date2num, num2date
# import pandas as pd

# from turtle import TurTleIndex
# import tushare as ts
# import pandas as pf, tushare as ts

# from turtle import TurTleIndex

