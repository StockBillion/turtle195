#!/usr/bin/env python
#-*- coding: utf8 -*-
import argparse
import pandas as pf
import tushare as ts


# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

class StockDataSet:
    '股票数据集合'
    stocks = {}
    
    def join(self, data1, data2):
        len1 = len(data1)
        len2 = len(data2)

        if len1 < 1: 
            return data2
        if len2 < 1: 
            return data1

        _head1 = str(data1.at[0, 'trade_date'])
        _head2 = str(data2.at[0, 'trade_date'])
        _tear1 = str(data1.at[len1-1, 'trade_date'])
        _tear2 = str(data2.at[len2-1, 'trade_date'])

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
        else:
            if _tear1 < _tear2 :
                data0 = data1
            else:
                data0 = data2

        return data0

    def read(self, code):
        try:
            self.stocks[code] = pf.read_csv('./data/' + code + '.csv', index_col=0)
            return self.stocks[code]
        except IOError: 
            return pf.DataFrame()

    def load(self, code, startdate, enddate):
        print( 'load stock ' + code + ' data')
        local_data = self.read(code)
        _rowcount = len(local_data)

        if _rowcount > 0 :
            _head = str(local_data.at[ 0, 'trade_date'])
            _tear = str(local_data.at[_rowcount-1, 'trade_date'])

            if _head < enddate :
                down_data = pro.daily(ts_code=code, start_date=str(local_data.at[ 0, 'trade_date'] + 1), end_date=enddate)
                local_data = self.join(local_data, down_data)
            if _tear > startdate :
                down_data = pro.daily(ts_code=code, start_date=startdate, end_date=_tear)
                local_data = self.join(local_data, down_data)
        else:
            local_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)

        print(local_data)
        self.stocks[code] = local_data
        self.stocks[code].to_csv('./data/' + code + '.csv')
        
        
if __name__ == "__main__":
    dataset = StockDataSet()
    startdate = '20180101'
    enddate = '20181201'

    parser = argparse.ArgumentParser(description="show example")
    parser.add_argument('filename', default=['601857.sh'], nargs='*')
    parser.add_argument("-s", "--start_date", help="start date")
    parser.add_argument("-e", "--end_date", help="end date")

    ARGS = parser.parse_args()
    if ARGS.start_date:
        startdate = str(ARGS.start_date)
    if ARGS.end_date:
        enddate = str(ARGS.end_date)
    if ARGS.filename:
        stock_codes = ARGS.filename

    for code in stock_codes:
        dataset.load(code, startdate, enddate)

    # opts,args = getopt.getopt(sys.argv[1:], "e:hs:v", ['end=', 'help', 'start=', 'version'])
    # # opts, args = getopt.getopt(sys.argv[1:], "hvs:e:", ['help', 'version', 'start=', 'end='])
    # print(sys.argv[1:])
    # print(opts)

    # for opt_name, opt_value in opts:
    #     print(opt_name)
    #     print(opt_value)
    #     if opt_name in ('-h','--help'):
    #         sys.exit()
    #     elif opt_name in ('-v','--version'):
    #         sys.exit()
    #     elif opt_name in ('-s','--start'):
    #         startdate = opt_value
    #     elif opt_name in ('-e','--end'):
    #         enddate = opt_value

    # print(code)
    # print(startdate)
    # print(enddate)


        # down_data = pro.daily(ts_code=code, start_date=startdate, end_date=enddate)
        # self.stocks[code] = self.join(local_data, down_data)
        # down_data = down_data.sort_index(ascending=False)
        # down_data.to_csv('./data/' + code + '.csv')
        # self.stocks[code] = down_data

# import sys, getopt

            # print(_head)
            # type(_head)

            # print(enddate)
            # type(enddate)
