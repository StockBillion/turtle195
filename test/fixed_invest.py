#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, numpy as np
from matplotlib.pylab import date2num, num2date
import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
# import pandas as pf

from movingave import moving_average
from stockdata import StockDataSet, parse_stock_data
from account import StockAccount

fixed_invest = 3000.0

def fixed_invest_test(account, code, stock_data, stype = 'stock'):

    _date = datetime.datetime.strptime('20080101', '%Y%m%d')
    start_date = date2num(_date)

    dates, data_list, ave_price, volumes = parse_stock_data(stock_data)
    m120 = moving_average(ave_price, 240)
    m480 = moving_average(ave_price, 480)

    market_values = []
    month = 0
    up120 = False
    up480 = False

    for n in range(0, len(stock_data)):
        _date, _open, _high, _low, _close = data_list[n][0:5]
        if stype == 'index':
            _open /= 1000
            _close/= 1000

        if _date < start_date:
            account.UpdateValue({code: _close})
            market_values.append(account.market_value *.01)
            continue

        _month = num2date(_date).month
        if _month != month:
            month = _month
            account.Rechange(fixed_invest)

            if not up480:
                if account.cash > fixed_invest*2:
                    volume = fixed_invest*2 / _open
                else:
                    volume = fixed_invest / _open
                # volume = fixed_invest / _open
                volume = int(volume/100) * 100
                account.Order(code, _open, volume, _date)

        if m120[n] < data_list[n][2]:
            _up120 = True
        else:
            _up120 = False

        if m480[n] < data_list[n][2]:
            up480 = True
        else:
            up480 = False

        if up480 and up120 and not _up120:
            volume = account.stocks.at[code, 'volume']
            account.Order(code, _open, -volume, _date)
        up120 = _up120

        account.UpdateValue({code: _close})
        market_values.append(account.market_value *.01)

    fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    # plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8，hspace=0.2, wspace=0.3)

    ax1.xaxis_date()
    ax1.set_title(code)
    ax1.set_ylabel("price")

    plt.xticks(rotation=45)
    plt.yticks()

    mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')
    ax1.plot(dates, market_values, color='r', lw=2, label='MV')
    ax1.plot(dates, m120, color='y', lw=2, label='MA (120)')
    ax1.plot(dates, m480, color='b', lw=2, label='MA (480)')

    ax2.bar(dates, volumes, width=0.75)
    ax2.set_ylabel('Volume')

    plt.xlabel("date")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    dataset = StockDataSet()
    account = StockAccount(0)

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
        fixed_invest_test(account, code, dataset.stocks[code], stype)
        print(account.cash, account.market_value)



    # market_values = []
    # print(data_list)
    # print(ave_price)
    # print(volumes)

    # data_table = np.transpose( data_list )
    # dates = data_table[0]
    # ax1.plot(dates, m120, color='g', lw=2, label='MA (120)')
    # ax1.plot(dates, m020, color='b', lw=2, label='MA (20)')
