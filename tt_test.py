#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, datetime as dt
from matplotlib.pylab import date2num, num2date
from stock_utils import StockDataSet, StockDisp, StockAccount
from ttindex import TurTleIndex


if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20130101'
    enddate = '20190101'

    loss_unit = 0.01
    long_cycle = 55
    short_cycle= 20
    index_codes = ['000300.sh']
    # index_codes = ['000300.sh', '399673.sz']
    # index_codes = ['000001.sh', '000300.sh', '000905.sh', '399673.sz']

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument('stock_codes', default=['000300.sh'], nargs='*')
    # parser.add_argument("-s", "--start_date", help="start date")
    # parser.add_argument("-e", "--end_date", help="end date")
    # parser.add_argument("-t", "--data_type", help="data type")
    # parser.add_argument("-u", "--time_unit", help="time unit")
    parser.add_argument("-l", "--loss_unit", help="loss unit")

    ARGS = parser.parse_args()
    # if ARGS.start_date:
    #     startdate = str(ARGS.start_date)
    # if ARGS.end_date:
    #     enddate = str(ARGS.end_date)
    # if ARGS.data_type:
    #     stype = str(ARGS.data_type)
    # if ARGS.time_unit:
    #     time_unit = ARGS.time_unit
    if ARGS.loss_unit:
        loss_unit = float(ARGS.loss_unit)
        # loss_unit *= 0.001
    if ARGS.stock_codes:
        stock_codes = ARGS.stock_codes

    _date = dt.datetime.strptime('20080101', '%Y%m%d')
    start_date = date2num(_date)
    _date = dt.datetime.strptime('20190101', '%Y%m%d')
    end_date = date2num(_date)

    for code in index_codes:
        index_data = dataset.load(code, startdate, enddate, 'index', 'daily')
        dates, data_list, ave_price, volumes = dataset.parse_data(code)
        # dates, data_list, ave_price, volumes = parse_stock_data( index_data )
        turtle = TurTleIndex(data_list, long_cycle, short_cycle, 1, 3)

        dates = turtle.data['date']
        closes = turtle.data['close']
        long_counts = turtle.data['state']
        keyprice = turtle.data['key_prices']
        Nl = turtle.data['long_wave']
        # NS = turtle.data['short_wave']

        account = StockAccount(100000, 0)
        count = 0
        cash_unit = account.cash
        market_values = []
        market_values.append(account.market_value)
        account.ProfitDaily()

        for i in range(1, len(closes)):
            account.ProfitDaily()
            kp = keyprice[i]*0.01
            _date = dates[i]

            if _date < start_date or _date > end_date:
                account.UpdateValue({code: closes[i]*0.01})
                market_values.append(account.market_value)
                # stock_volumes.append(0)
                continue

            if count < long_counts[i] and count < 4:
                count = long_counts[i]
                if count == 1:
                    cash_unit = account.cash * loss_unit * keyprice[i] / Nl[i]
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
        account.save_records('./data', 'tt-'+code)
        turtle.save_data('./data', 'tt-'+code)
        # print( account.get_records() )

        # plot = StockDisp(code)
        # plot.LogKDisp(plot.ax1, data_list)
        # plot.LogPlot(plot.ax1, dates, market_values, 'r', 5)
        # # plot.LogPlot(plot.ax1, dates, keyprice, 'r')
        # plot.LogPlot(plot.ax2, dates, NS, 'r')
        # plot.Plot(plot.ax2, dates, long_counts, 'B')
        # plot.show()


