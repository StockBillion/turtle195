#!/usr/bin/env python
#-*- coding: utf8 -*-
import pandas as pf
import tushare as ts
# import pandas.core.frame as pf

# https://tushare.pro/
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

# hist_data = pro.index_daily(ts_code='000001.SH', start_date='20180901')
# print(hist_data)
# exit(0)

class StockDataSet:
    '股票数据集合'
    stocks = {}
    
    def load(self, code):
        hist_data = pro.daily(ts_code='601857.SH', start_date='20180901', end_date='20181201')
        hist_data = hist_data.sort_index(ascending=False)

        hist_data.to_csv('./data/' + code + '.csv')
        self.stocks[code] = hist_data

    def read(self, code):
        self.stocks[code] = pf.read_csv('./data/' + code + '.csv', index_col=0)


class StockAccount:
    '股票交易账户'
    market_value = 0
    cash = 0
    cost = 0
    stocks = pf.DataFrame()

    def __init__(self, cash):
        self.cash = cash

    def prt(self):
        print( "total balance = " , (self.market_value + self.cash), \
            "\nmarket value = " , self.market_value, "\ncapital = " , self.cash )

    def Rechange(self, _cash):
        self.cash += _cash

    def Cash(self, _capital):
        if( self.cash >= _capital ):
            self.cash -= _capital
        else:
            raise ValueError("Insufficient account balance")

    def Order(self, code, name, price, volume):
        _value = price*volume
        if( self.cash - _value < 0 ):
            raise ValueError("not sufficient funds.")
        self.cash -= _value

        absv = abs(_value)
        if absv * 0.001 < 5:
            _cost = 5
        else:
            _cost = absv * 0.001

        if volume < 0:
            _cost += absv * 0.001
        _cost += absv * 0.00002
        self.cost += _cost

        if  code in self.stocks.index : 
            if( self.stocks.loc[code]['volume'] + volume < 0 ):
                raise ValueError("Don't naked short sale.")
            _row = self.stocks.loc[code]
            _volume = _row.volume + volume
            if _volume == 0:
                _cost = _row.cost
            else:
                _cost = (_row.volume*_row.cost + _cost + _value) / _volume
            # _cost = price*volune + _row.volume*_row.cost
            self.stocks.loc[code] = [name, _volume, _cost, _volume*price]

        else:
            if( volume <= 0 ):
                raise ValueError("Don't naked short sale.")
            _cost = (_cost + _value) / volume
            _row = {'name': [name], 'volume': [volume], 'cost': [_cost], 'market_value': [_value]}
            _index = [code]
            self.stocks = self.stocks.append(pf.DataFrame(_row, _index))


acc1 = StockAccount(10000)
acc1.Order("601857", "zhongguoshiyou", 7.7, 400)
acc1.Order("601318", "zhongguopingan", 62.18, 100)
acc1.Order("601857", "zhongguoshiyou", 7.5, -200)
print(acc1.cash, acc1.cost)
print(acc1.stocks)

dataset = StockDataSet()
dataset.read('601857')
print(dataset.stocks['601857'])

# acc1.stocks.to_csv('./data/account.csv')


# print(acc1.stocks.loc['601318'])


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


    # stocks = []
    # stocks = pf.DataFrame(columns=['name', 'volume', 'market_value'])
            # self.stocks.loc[code] = {'name': [name], 'volume': [volume], 'market_value': [_value]}
            # [name, volume, volume*price]

        # _row = {'code': [code], 'name': [name], 'volume': [volume], 'market_value': [_value]}
        # self.stocks = self.stocks.append(pf.DataFrame(_row), ignore_index=True)
        
            # _row.volume += volume
            # _row.market_value = _row.volume *price
            # self.stocks.update(_row)
            # self.stocks.loc[code] = _row
            # self.stocks.loc[code]['volume'] += volume
            # self.stocks.loc[code]['market_value'] = self.stocks.loc[code]['volume'] * price
            
        # _row = [code, name, volume, _value]
        # _row = {'code': code, 'name': name, 'volume': volume, 'market_value': _value}
        # self.stocks.append(_row)

        # _row = pf.DataFrame([[code], [name], [volume], [_value]], columns=['code','name','volume', 'market_value'])
        # _row = pf.DataFrame({'code': code, 'name': name, 'volume': volume, 'market_value': _value})

        # _row = pf.DataFrame(_row)
        # print(_row)
        # self.stocks.append({'code': code, 'name': name, 'volume': volume, 'market_value': _value}, ignore_index=True)

        #     if -_value * 0.002 < 5:
        #         _cost += 5
        #     else
        #         _cost = _value * 0.001    
        #     _cost = -_value * 0.002
        # else:
        #     _cost = _value * 0.001

# df2 = pf.read_csv('./data/account.csv', index_col=0)
# print(df2)
# exit(0)
