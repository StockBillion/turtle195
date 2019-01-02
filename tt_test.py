#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse
from stock_utils import StockDataSet, parse_stock_data, StockAccount
from ttindex import TurTleIndex


if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20130101'
    enddate = '20190101'

    loss_unit = 0.01
    long_cycle = 55
    short_cycle= 20
    index_codes = ['000300.sh']
    # index_codes = ['000001.sh', '000300.sh', '000905.sh', '399673.sz']

    for code in index_codes:
        index_data = dataset.load(code, startdate, enddate, 'index', 'daily')
        dates, data_list, ave_price, volumes = parse_stock_data(index_data)
        turtle = TurTleIndex(data_list, long_cycle, short_cycle, 1, 2)

        dates = turtle.data['date']
        closes = turtle.data['close']
        long_counts = turtle.data['state']
        keyprice = turtle.data['key_prices']
        NS = turtle.wave[short_cycle]

        account = StockAccount(100000, 500000)
        count = 0
        cash_unit = account.cash
        market_values = []

        for i in range(1, len(closes)):
            account.ProfitDaily()
            kp = keyprice[i]*0.01
            
            if count < long_counts[i] and count < 4:
                count = long_counts[i]
                if count == 1:
                    cash_unit = account.cash * loss_unit * keyprice[i] / NS[i]
                volume = cash_unit / kp
                if volume >= 100: 
                    account.Order(code, kp, volume, dates[i])

            if count and not long_counts[i]:
                count = long_counts[i]
                volume = account.stocks.at[code, 'volume']
                account.Order(code, kp, -volume, dates[i])

            account.UpdateValue({code: closes[i]*0.01})
            market_values.append(account.market_value)

        account.status_info()
        account.save_records('./data', code)
        print( account.get_records() )


                # print(volume, kp, cash_unit)
                # print(account.stocks)
                # print(count, long_counts[i])
                # print(account.stocks)
        # turtle.print_records()
        # data_list = log_list(data_list, turtle.low_prices[120][len(data_list)-1])
        # mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='red', colordown='green')
        # ax2.plot(dates, turtle.strong[120], lw=2, label='wave')
