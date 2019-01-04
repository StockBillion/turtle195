#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, datetime as dt
from matplotlib.pylab import date2num, num2date
from ttindex import TurTleIndex
from stock_utils import StockDataSet, StockDisp, StockAccount


if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20130101'
    enddate = '20190101'

    loss_unit = 0.01
    append = 1
    stop_loss = 3

    long_cycle = 55
    short_cycle= 20
    index_codes = ['000001.sh', '000300.sh', '000905.sh', '399673.sz']

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument('stock_codes', default=['000001.sh', '000300.sh', '000905.sh', '399673.sz'], nargs='*')
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")
    parser.add_argument("-a", "--append", help="append")
    parser.add_argument("-l", "--stop_loss", help="stop loss")
    parser.add_argument("-u", "--loss_unit", help="loss unit")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = str(ARGS.start_date)
    if ARGS.end_date:
        enddate = str(ARGS.end_date)

    if ARGS.loss_unit:
        loss_unit = float(ARGS.loss_unit)
    if ARGS.append:
        append = float(ARGS.append)
    if ARGS.stop_loss:
        stop_loss = float(ARGS.stop_loss)

    if ARGS.stock_codes:
        index_codes = ARGS.stock_codes

    _date = dt.datetime.strptime(startdate, '%Y%m%d')
    start_date = date2num(_date)
    _date = dt.datetime.strptime(enddate, '%Y%m%d')
    end_date = date2num(_date)

    b_dates = []
    turtles = {}
    indexs = {}
    counts = {}

    date_vecs = {}
    states = {}
    closes = {}
    keyprices = {}
    Nls = {}

    for code in index_codes:
        index_data = dataset.load(code, startdate, enddate, 'index', 'daily')
        dates, data_list, ave_price, volumes = dataset.parse_data(code)
        turtles[code] = TurTleIndex(data_list, long_cycle, short_cycle, append, stop_loss)
        turtles[code].save_data('./data', 'tt-'+code)

        indexs[code] = 0
        counts[code] = 0

        date_vecs[code] = turtles[code].data['date']
        states[code] = turtles[code].data['state']
        closes[code] = turtles[code].data['close']
        keyprices[code] = turtles[code].data['key_prices']
        Nls[code] = turtles[code].data['long_wave']

        if len(b_dates) < len(dates):
            b_dates = dates

    account = StockAccount(100000, 0)
    count = 0
    first = ''
    cash_unit = account.cash

    market_values = []
    market_values.append(account.market_value)
    account.ProfitDaily()

    for _idx in range(1, len(b_dates)):
        account.ProfitDaily()
        _date = b_dates[_idx]
        _close = {}

        if _date < start_date or _date > end_date:
            market_values.append(account.market_value)
            continue

        # _time_str = num2date(_date).strftime('%Y%m%d')
        # _count_str = ''
        # for code in index_codes:
        #     _count_str += ' ' + str( counts[code] )
        # print(_time_str, first, _count_str, count)

        for code in index_codes:
            dates = date_vecs[code]
            while indexs[code] < len(dates) and dates[indexs[code]] < _date:
                indexs[code] += 1
            if indexs[code] > len(dates): 
                continue
            _close[code] = closes[code][indexs[code]] * 0.01
            _kp = keyprices[code][indexs[code]] * 0.01
            _state = states[code][indexs[code]]

            if counts[code] < _state and count < 4:
                if not count:
                    cash_unit = account.cash * loss_unit * _kp*100 / Nls[code][indexs[code]]
                    first = code
                volume = cash_unit / _kp
                if first == code and volume >= 100:
                    count += 1
                    counts[code] = _state
                    account.Order(code, _kp, volume, _date)

            elif first == code and count > 0 and not _state:
                first = ''
                count = 0
                # count -= counts[code]
                counts[code] = _state
                if code in account.stocks.index:
                    volume = account.stocks.at[code, 'volume']
                    account.Order(code, _kp, -volume, _date)

        account.UpdateValue(_close)
        market_values.append(account.market_value)


    # plot = StockDisp(code)
    # plot.LogKDisp(plot.ax1, data_list)
    # plot.LogPlot(plot.ax1, dates, market_values, 'r', 4)
    # plot.LogPlot(plot.ax2, dates, Nl, 'r')
    # plot.Plot(plot.ax2, dates, long_counts, 'B')
    # plot.show()

    account.status_info()
    # account.save_records('./data', 'tt-first')
    # print( account.get_records() )


