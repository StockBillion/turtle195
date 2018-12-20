#!/usr/bin/env python
#-*- coding: utf8 -*-
import numpy as np
from matplotlib.pylab import date2num, num2date
import pandas as pf
import tushare as ts

index_code = '000300.sh'
stock_codes = ['601398.sh', '601988.sh', '601628.sh', '600028.sh', '600036.sh', '601318.sh', 
	'601328.sh', '600000.sh', '601998.sh', '601166.sh', '600030.sh', '600016.sh', 
	'600519.sh', '600019.sh', '600050.sh', '600104.sh', '601006.sh', '600018.sh', 
	'000858.sz', '601111.sh', '000002.sz', '600900.sh', '601601.sh', '601991.sh' ]

# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

# df = pro.index_weight(index_code='399300.SZ', start_date='20180901', end_date='20180930')
# print(df)

if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20180101'
    enddate = '20181201'
    stype = 'stock'

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = ARGS.start_date
    if ARGS.end_date:
        enddate = ARGS.end_date
