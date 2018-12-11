#!/usr/bin/python
#-*- coding: utf8 -*-
import pandas.core.frame as pf

class StockAccount:
    '股票交易账户'
    market_value = 0
    cash = 0
    # stocks = []
    stocks = pf.DataFrame()
    # stocks = pf.DataFrame(columns=['name', 'volume', 'market_value'])

    def __init__(self, cash):
        self.cash = cash

    def Buy(self, code, name, price, volume):
        if( self.cash < price*volume ):
            raise ValueError("not sufficient funds.")
        _value = price*volume
        self.cash -= _value
        _row = {'name': [name], 'volume': [volume], 'market_value': [_value]}
        _index = [code]
        self.stocks = self.stocks.append(pf.DataFrame(_row, _index))
        # _row = {'code': [code], 'name': [name], 'volume': [volume], 'market_value': [_value]}
        # self.stocks = self.stocks.append(pf.DataFrame(_row), ignore_index=True)
        

acc1 = StockAccount(10000)
acc1.Buy("601857", "zhongguoshiyou", 7.7, 400)
acc1.Buy("601318", "zhongguopingan", 62.18, 100)
print(acc1.cash)
print(acc1.stocks)


# https://tushare.pro/
# import tushare as ts
# ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
# pro = ts.pro_api()

# hist_data = pro.fund_daily(ts_code='150018.SZ', 
#     start_date='20180101', end_date='20181208')

# hist_data.info()
# print(hist_data)


    # stocks = pf.DataFrame()
# df1 = pf.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
# df2 = pf.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
# print(df1)
# print(df2)
# df1 = df1.append(df2, ignore_index=True)
# print(df1)


        # _row = [code, name, volume, _value]
        # _row = {'code': code, 'name': name, 'volume': volume, 'market_value': _value}
        # self.stocks.append(_row)

        # _row = pf.DataFrame([[code], [name], [volume], [_value]], columns=['code','name','volume', 'market_value'])
        # _row = pf.DataFrame({'code': code, 'name': name, 'volume': volume, 'market_value': _value})

        # _row = pf.DataFrame(_row)
        # print(_row)
        # self.stocks.append({'code': code, 'name': name, 'volume': volume, 'market_value': _value}, ignore_index=True)
