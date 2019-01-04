#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np, pandas as pd, math
import matplotlib.pyplot as plt, mpl_finance as mpf
from matplotlib.pylab import date2num, num2date
from stock_utils import StockDataSet, MovingAverage


class TurTleIndex:
    '海龟指标'

    def __init__(self, data_list):
        data_table = np.transpose( data_list )

        self.data = {}
        self.wave = {}

        self.high_prices = {}
        self.high_locats = {}
        self.low_prices = {}
        self.low_locats = {}

        self.date_str = []
        for i in range(0, len(data_table[0])):
            datestr = num2date(data_table[0][i]).strftime('%Y%m%d')
            self.date_str.append(datestr)

        self.data['date'] = data_table[0]
        self.data['date_str'] = self.date_str
        self.data['open'] = data_table[1]
        self.data['high'] = data_table[2]
        self.data['low' ] = data_table[3]
        self.data['close'] = data_table[4]

    # def __init__(self, data_list, long_period, short_period, append_multiple, loss_multiple):
    #     data_table = np.transpose( data_list )

    #     self.data = {}
    #     self.wave = {}

    #     self.high_prices = {}
    #     self.high_locats = {}
    #     self.low_prices = {}
    #     self.low_locats = {}

    #     self.date_str = []
    #     for i in range(0, len(data_table[0])):
    #         datestr = num2date(data_table[0][i]).strftime('%Y%m%d')
    #         self.date_str.append(datestr)

    #     self.data['date'] = data_table[0]
    #     self.data['date_str'] = self.date_str
    #     self.data['open'] = data_table[1]
    #     self.data['high'] = data_table[2]
    #     self.data['low' ] = data_table[3]
    #     self.data['close'] = data_table[4]

    #     self.price_wave(long_period, short_period)
    #     self.long_trade(long_period, short_period, append_multiple, loss_multiple)

    def print_records(self):
        print( pd.DataFrame(self.data) )

    def save_data(self, path, code):
        records = pd.DataFrame(self.data)
        records.to_csv(path + '/' + code + '.ttindex.csv')

    def price_wave(self, long_period, short_period):
        price_wave = self.data['high'] - self.data['low']
        wavema = MovingAverage(price_wave)
        self.wave[1] = price_wave
        self.wave[long_period ] = wavema.moving_average(long_period)
        self.wave[short_period] = wavema.moving_average(short_period)
        self.data['long_wave' ] = self.wave[long_period ]
        self.data['short_wave'] = self.wave[short_period]


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

    def stort_index(self, period):
        _vulnerable = []
        close = self.data['close']

        high = self.data['high']
        self._highest_price(high, period)
        HP1 = self.high_prices[period]

        _vulnerable.append(0)
        for i in range(1, len(close)):
            v = (close[i] - HP1[i])/HP1[i]
            _vulnerable.append(v*100)
        return _vulnerable

    def long_index(self, period):
        _strong = []
        close = self.data['close']

        low  = self.data['low' ]
        self._lowest_price (low , period)
        LP1 = self.low_prices [period]

        _strong.append(0)
        for i in range(1, len(close)):
            s = (close[i] - LP1[i])/LP1[i]
            _strong.append(s*100)
        return _strong

    def long_trade(self, long_period, short_period, append_multiple, loss_multiple, max_long_count = 4):
        state = []
        key_prices = []
        long_count = 0
        keyprice = 0
        keyN = 0

        self._highest_price(self.data['high'], long_period)
        self._lowest_price (self.data['low' ], short_period)

        self.data['long_high'] = self.high_prices[long_period]
        self.data['short_low'] = self.low_prices[short_period]

        Hl = self.high_prices[long_period]
        Ls = self.low_prices[short_period]
        Nl = self.wave[long_period]
        
        open = self.data['open']
        high = self.data['high']
        low  = self.data['low' ]

        for i in range(0, long_period):
            state.append(long_count)
            key_prices.append(0)

        for i in range(long_period, len(high)):
            if long_count > 0:
                append_price = keyprice + keyN * append_multiple
                stop_price = max(Ls[i], keyprice - keyN * loss_multiple)
                # stop_price = max(Ls[i], keyprice - Ns[i] * loss_multiple + keyN - Ns[i])
            else:
                append_price = Hl[i]
                stop_price = Ls[i]

            if long_count > 0 and low[i] < stop_price:
                long_count = 0
                if open[i] < stop_price:
                    keyprice = open[i]
                else:
                    keyprice = stop_price
                # print('short', dates[i], open[i], low[i], long_count, stop_price)

            elif high[i] > append_price and long_count < max_long_count:
                # keyN = Nl[i]
                if not long_count:
                    keyN = Nl[i]

                long_count += 1
                if open[i] > append_price:
                    keyprice = open[i]
                else:
                    keyprice = append_price
                # print('long ', dates[i], open[i], high[i], long_count, append_price)

            state.append(long_count)
            key_prices.append(keyprice)

        self.data['state'] = state
        self.data['key_prices'] = key_prices
        # print('trade count', len(high), len(key_prices))

    def short_trade(self, long_period, short_period, append_multiple, loss_multiple, max_long_count = 4):
        state = []
        key_prices = []
        long_count = 0
        keyprice = 0
        keyN = 0

        self._highest_price(self.data['high'], short_period)
        self._lowest_price (self.data['low' ], long_period)

        self.data['long_short'] = self.low_prices[long_period]
        self.data['short_high'] = self.high_prices[short_period]

        Ll = self.low_prices[long_period]
        Hs = self.high_prices[short_period]
        Nl = self.wave[long_period]
        
        open = self.data['open']
        high = self.data['high']
        low  = self.data['low' ]

        for i in range(0, long_period):
            state.append(long_count)
            key_prices.append(0)

        for i in range(long_period, len(high)):
            if long_count > 0:
                append_price = keyprice - keyN * append_multiple
                stop_price = max(Hs[i], keyprice + keyN * loss_multiple)
                # stop_price = max(Ls[i], keyprice - Ns[i] * loss_multiple + keyN - Ns[i])
            else:
                append_price = Ll[i]
                stop_price = Hs[i]

            if long_count > 0 and high[i] > stop_price:
                long_count = 0
                if open[i] > stop_price:
                    keyprice = open[i]
                else:
                    keyprice = stop_price
                # print('short', dates[i], open[i], low[i], long_count, stop_price)

            elif low[i] < append_price and long_count < max_long_count:
                # keyN = Nl[i]
                if not long_count:
                    keyN = Nl[i]
                long_count += 1
                if open[i] < append_price:
                    keyprice = open[i]
                else:
                    keyprice = append_price
                # print('long ', dates[i], open[i], high[i], long_count, append_price)

            state.append(long_count)
            key_prices.append(keyprice)

        self.data['state'] = state
        self.data['key_prices'] = key_prices
        # print('trade count', len(high), len(key_prices))



        # self.strong = {}
        # self.strong_index(120)
        # self.data['strong_index'] = self.strong[120]

            # s = (HP1[i] - LP3[i])/LP3[i] + (LP1[i] - HP3[i])/HP3[i]
            # s = (high[i] - LP[i])/LP[i] + (low[i] - HP[i])/HP[i]
            # s = (close[i] - LP[i]) / (i - LL[i]) + (close[i] - HP[i]) / (i - HL[i])

            # if long_count > 0 and high[i] < stop_price:
            #     long_count = 0
            #     keyprice = close[i]

            #     while high[i] > append_price and long_count < max_long_count:
            #         long_count += 1
            #         if open[i] > append_price:
            #             keyprice = open[i]
            #         else:
            #             keyprice = append_price
            #         state.append(long_count)
            #         key_prices.append(keyprice)
            #         append_price = keyprice + keyN * append_multiple

            # else:
            #     state.append(long_count)
            #     key_prices.append(keyprice)


            # print(self.data['date'][i], high[i], low[i], sl[i], lh[i], N[i], 
            #     stop_price, append_price, long_count, keyprice)

            # keyN = Ns[i]
            # stop_price = max(SL[i], keyprice - SN[i] * loss_multiple)
            # append_price = max(lh[i], keyprice + N[i] * append_multiple)

        # self._highest_price(high, period*3)
        # self._lowest_price (low , period*3)
        # HP3 = self.high_prices[period*3]
        # LP3 = self.low_prices [period*3]

        # HP = self.high_prices[period]
        # LP = self.low_prices [period]
        # HL = self.high_locats[period]
        # LL = self.low_locats [period]

        # self.strong_index(5)
        # self.strong_index(20)

        # print( pd.DataFrame(self.strong)[220: 250] )
        # print( pd.DataFrame(self.data)[220: 250] )

        # self.data['lh_locat'] = self.high_locats[10]
        # self.data['ll_locat'] = self.low_locats[10]

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


# def log_list(data_list, base0 = 1):
#     _b = math.log(base0)
#     for i in range(0, len(data_list)):
#         # data_list[i] = math.log(data_list[i]) - _b
#         date, open, high, low, close = data_list[i]
#         open = math.log(open) - _b
#         high = math.log(high) - _b
#         low = math.log(low) - _b
#         close = math.log(close) - _b
#         data_list[i] = (date, open, high, low, close)
#     return data_list


# if __name__ == "__main__":
#     dataset = StockDataSet()
#     startdate = '20170101'
#     enddate = '20190101'

#     long_cycle = 55
#     short_cycle= 20
#     stock_datas = {}

#     parser = argparse.ArgumentParser(description="show example")
#     parser.add_argument("-s", "--start_date", help="start date")
#     parser.add_argument("-e", "--end_date", help="end date")

#     ARGS = parser.parse_args()
#     if ARGS.start_date:
#         startdate = ARGS.start_date
#     if ARGS.end_date:
#         enddate = ARGS.end_date


#     fig,[ax1,ax2] = plt.subplots(2, 1, sharex=True)
#     fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
#     # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)

#     ax1.xaxis_date()
#     ax1.set_title('indexs')
#     ax1.set_ylabel("price")
#     ax2.set_ylabel('Volume')

#     plt.xticks(rotation=45)
#     plt.yticks()
#     plt.xlabel("date")


#     for code in index_codes:
#         index_data = dataset.load(code, startdate, enddate, 'index', 'daily')
#         dates, data_list, ave_price, volumes = parse_stock_data(index_data)
#         turtle = TurTleIndex(data_list, long_cycle, short_cycle, 1, 2)

#         data_list = log_list(data_list, turtle.low_prices[120][len(data_list)-1])
#         mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='red', colordown='green')
#         ax2.plot(dates, turtle.strong[120], lw=2, label='wave')

#     # ax1.plot(dates, h55, color='y', lw=2, label='high (long_cycle)')
#     # ax1.plot(dates, l20, color='b', lw=2, label='low (short_cycle)')
#     # ax1.plot(dates, avma240, color='g', lw=2, label='MA (240)')
#     # ax1.plot(dates, market_values, color='r', lw=2, label='MV')
#     # ax2.bar(dates, volumes, width=0.75)
#     # ax2.plot(dates, stock_volumes, color='r', lw=2, label='volumes')

#     # ax2.plot(dates, turtle.strong[5], color='r', lw=2, label='wave')
#     # ax2.plot(dates, turtle.strong[20], color='g', lw=2, label='wave')
#     # ax2.plot(dates, turtle.strong[60], color='b', lw=2, label='wave')
    
#     plt.grid()
#     plt.show()
    # plt.savefig("./images/turtle2055.png")


# from enum import Enum

## 准备数据
    # index_data = dataset.load(index_code, startdate, enddate, 'index', 'daily')
    # for code in stock_codes:
    #     stock_datas[code] = dataset.load(code, startdate, enddate, 'stock', 'daily')

# ## 计算指标
    # calc_ttindex(index_data, long_cycle, short_cycle, 1, 2)
#     for code in stock_codes:
# 		calc_ttindex(stock_datas[code], long_cycle, short_cycle)


    # turtle = TurTleIndex(data_list, long_cycle, short_cycle, 1, 2)
    # h55 = turtle.high_prices[55]
    # l20 = turtle.low_prices[20]
    # strong = turtle.strong[120]

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


        # self._highest_price(self.data['high'], 40)
        # self._highest_price(self.data['high'], 120)
        # self._lowest_price (self.data['low' ], 40)
        # self._lowest_price (self.data['low' ], 120)

        # strong10 = []
        # strong10 


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


# # https://tushare.pro/
# ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
# pro = ts.pro_api()

# df = pro.index_weight(index_code='399300.SZ', start_date='20180901', end_date='20180930')
# print(df)

# class StrongIndex:
#     '强弱指标'
#     def __init__(self)
