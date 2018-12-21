#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np
from matplotlib.pylab import date2num, num2date
import pandas as pf
from turtle import TurTleIndex
# import tushare as ts
# import pandas as pf, tushare as ts

from stockdata import StockDataSet, parse_stock_data
from account import StockAccount
from movingave import MovingAverage
from turtle import TurTleIndex


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

## 计算指标
def calc_ttindex(data_frame, long_cycle, short_cycle):
    dates, data_list, ave_price, volumes = parse_stock_data(data)
    data_table = np.transpose( data_list )
    wavema = MovingAverage(data_table[2] - data_table[3], short_cycle)
    wvma20 = wavema.ma_indexs[short_cycle]

    turtle = TurTleIndex(data_table[2], data_table[3], long_cycle, short_cycle)
    h55 = turtle.high_indexs[long_cycle]
    l20 = turtle.low_indexs[short_cycle]


if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20180101'
    enddate = '20181201'

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
    for code in stock_codes:
        stock_datas[code] = dataset.load(code, startdate, enddate, 'stock', 'daily')

## 计算指标
	calc_ttindex(index_data, long_cycle, short_cycle)
    for code in stock_codes:
		calc_ttindex(stock_datas[code], long_cycle, short_cycle)

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


