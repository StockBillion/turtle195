#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, sys, numpy, datetime as dt, time
from ttindex import TurTleIndex
from stock_utils import StockDataSource, StockDisp, StockAccount

class StrongTurtleIndex:
    '强势海龟指标'

    def __init__(self, index_code, stocks):
        self.index_code = index_code
        self.stock_codes = stocks


if __name__ == "__main__":
    now_time = dt.datetime.now()
    # print(n)
    # print(n.month)
    yes_time = now_time + dt.timedelta(days=-180)
    print( yes_time.strftime('%Y-%m-%d') )

