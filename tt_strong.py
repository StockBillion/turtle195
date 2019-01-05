#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse, datetime as dt
from matplotlib.pylab import date2num, num2date
from ttindex import TurTleIndex
from stock_utils import StockDataSet, StockDisp, StockAccount



if __name__ == "__main__":
    dataset = StockDataSet()

    index_code = '000300.sh'
    # index_codes = ['000001.sh', '000300.sh', '000905.sh', '399673.sz']
    stock_codes = [
        '601398.sh', '601988.sh', '601628.sh', '600028.sh', '600036.sh', '601318.sh', 
        '601328.sh', '600000.sh', '601998.sh', '601166.sh', '600030.sh', '600016.sh', 
        '600519.sh', '600019.sh', '600050.sh', '600104.sh', '601006.sh', '600018.sh', 
        '000858.sz', '601111.sh', '000002.sz', '600900.sh', '601601.sh', '601991.sh',
        '601169.sh', '000001.sz', '000063.sz', '002024.sz', '601899.sh', '601939.sh',

        '600048.sh', '600837.sh', '601857.sh', '601668.sh', '601088.sh', '600031.sh',
        '600015.sh', '600795.sh', '600348.sh', '601600.sh', '601699.sh', '000651.sz',
        '000527.sz', '600585.sh', '000983.sz', '600276.sh', '600089.sh', '000538.sz',
        '000157.sz', '600832.sh', '600309.sh', '601666.sh', '601001.sh', '600547.sh',
        '000878.sz', '000629.sz', '002128.sz', '600663.sh', '002007.sz', '002202.sz',
        
        '600642.sh', '600383.sh', '600100.sh', '600208.sh', '000800.sz', '600887.sh',
        '600598.sh', '600518.sh', '600739.sh', '600583.sh', '600489.sh', '000060.sz',
        '000562.sz', '600875.sh', '601919.sh', '000937.sz', '601390.sh', '000402.sz',
        '600808.sh', '601333.sh', '000568.sz', '000933.sz', '600026.sh', '600027.sh', 
        '600256.sh', '600111.sh', '601168.sh', '600221.sh', '600655.sh', '601186.sh', 
        
        '600809.sh', '600011.sh', '600320.sh', '600177.sh', '000839.sz', '000401.sz', 
        '600150.sh', '000423.sz', '600123.sh', '600660.sh' ]
