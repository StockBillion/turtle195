#!/usr/bin/env python
#-*- coding: utf8 -*-
import sys, getopt
import pandas as pf
import tushare as ts


# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

class StockDataSet:
    '股票数据集合'
    stocks = {}
    
    def join(self, data1, data2):
        _head1 = data1.at[0, 'trade_date']
        _head2 = data2.at[0, 'trade_date']
        _tear1 = data1.at[-1, 'trade_date']
        _tear2 = data2.at[-1, 'trade_date']

        if( _head1 < _head2 ):
            if _tear1 < _tear2 :
                temp = data2.loc[data2['trade_date'] > _head1]
                data0 = temp.append(data1)
            else:
                data0 = data2
        elif _head1 > _head2 :
            if _tear1 < _tear2 :
                data0 = data1
            else:
                temp = data1.loc[data1['trade_date'] > _head1]
                data0 = temp.append(data2)
        return data0

    def read(self, code):
        self.stocks[code] = pf.read_csv('./data/' + code + '.csv', index_col=0)
        return self.stocks[code]

    def load(self, code, startdate, enddate):
        local_data = self.read(code)
        _head = local_data.at[0, 'trade_date']
        _tear = local_data.at[-1, 'trade_date']

        if _head < enddate :
            down_data = pro.daily(ts_code=code, start_date=_head, end_date=enddate)
            local_data = self.join(local_data, down_data)
        if _tear > startdate :
            down_data = pro.daily(ts_code=code, start_date=startdate, end_date=_tear)
            local_data = self.join(local_data, down_data)

        self.stocks[code] = local_data
        self.stocks[code].to_csv('./data/' + code + '.csv')
        
        
dataset = StockDataSet()
startdate = '20180101'
enddate = '20181201'

opts, args = getopt.getopt(sys.argv[1:], "hvs:e:", ['help', 'version', 'start=', 'end='])
for opt_name,opt_value in opts:
    if opt_name in ('-h','--help'):
        sys.exit()
    if opt_name in ('-v','--version'):
        sys.exit()
    if opt_name in ('-s','--start'):
        startdate = opt_value
    if opt_name in ('-e','--end'):
        enddate = opt_value

for code in args:
    dataset.load(code, startdate, enddate)


        # down_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
        # self.stocks[code] = self.join(local_data, down_data)
        # down_data = down_data.sort_index(ascending=False)
        # down_data.to_csv('./data/' + code + '.csv')
        # self.stocks[code] = down_data
