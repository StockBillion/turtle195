#-*- coding: utf8 -*-
from matplotlib.pylab import date2num
import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
# from matplotlib.font_manager import FontProperties

def moving_average(x, n, type='simple'): 
    x = np.asarray(x) 

    if type == 'simple': 
        weights = np.ones(n) 
    else: 
        weights = np.exp(np.linspace(-1., 0., n)) 

    weights /= weights.sum() 
    a = np.convolve(x, weights, mode='full')[:len(x)] 
    a[:n] = a[n] 
    
    return a

def highest_price(x, n):
    x = np.asarray(x) 
    hs = []
    hs.append(x[0])

    for i in range(1, len(x)):
        h = x[i-1]
        start = max(0, i-n)
        for j in range(start, i):
            h = max(h, x[j])
        hs.append(h)

    return hs

def lowest_price(x, n):
    x = np.asarray(x) 
    ls = []
    ls.append(x[0])

    for i in range(1, len(x)):
        l = x[i-1]
        start = max(0, i-n)
        for j in range(start, i):
            l = min(l, x[j])
        ls.append(l)

    return ls

# https://tushare.pro/
import tushare as ts

#在中国大陆使用pip进行python包安装的时候经常会出现socket.timeout: The read operation timed out的问题，下面就讲讲解决方案。
#>> 解决方案 <<

#使用国内镜像（以安装tushare pro为例）

#pip install tushare -i https://pypi.tuna.tsinghua.edu.cn/simple/
#// -i https://pypi.tuna.tsinghua.edu.cn/simple/
#// e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0
ts.set_token("e2a71ab976c499825f6f48186f24700f70e0f13af933e2f508684cc0")
pro = ts.pro_api()

# hist_data = pro.fund_daily(ts_code='150018.SZ', start_date='20180101', end_date='20181208')
# hist_data = pro.daily(ts_code='601857.SH', start_date='20180101', end_date='20181201')
hist_data = pro.daily(ts_code='601857.SH', start_date='20180101')
# hist_data = hist_data.reverse()

hist_data = hist_data.sort_index(ascending=False)
# hist_data = hist_data.sort_values(by=['trade_date'])

hist_data.info()
print(hist_data)
# exit(0)

data_list = []
ave_price = []
volumes = []

for rnum, row in hist_data.iterrows():
    tscode, date, open, high, low, close = row[0:6]
    vol,amount = row[9:11]
    _date = datetime.datetime.strptime(date, '%Y%m%d')
    timenum = date2num(_date)

    datas = (timenum,open,high,low,close)
    data_list.append(datas)
    ave_price.append( (high+low)/2 )
    volumes.append(vol)

# print( np.transpose( data_list ) )
print(data_list)
print(volumes)

# data_list = data_list.reverse()
data_table = np.transpose( data_list )
dates = data_table[0]

ma10 = moving_average(ave_price, 10, 'simple')
h20 = highest_price(data_table[2], 20)
l10 = highest_price(data_table[3], 10)

fig,[ax1,ax2] = plt.subplots(2,1,sharex=True)
# fig, ax1 = plt.subplots()
fig.subplots_adjust(bottom=0.2)

ax1.xaxis_date()
# ax1.xticks(rotation=45)
# ax1.yticks()

# plt.title("601857")
# ax1.set_xlabel("time")

ax1.set_title("601857")
ax1.set_ylabel("price")

plt.xticks(rotation=45)
plt.yticks()

# fig.ylabel("price")

mpf.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green')
ax1.plot(dates, ma10, color='c', lw=2, label='MA (10)')
ax1.plot(dates, h20, color='r', lw=2, label='highest (20)')
ax1.plot(dates, l10, color='y', lw=2, label='lowest (10)')

ax2.bar(dates, volumes, width=0.75)
ax2.set_ylabel('Volume')

plt.xlabel("date")
plt.grid()
plt.show()
# print("\n")

exit(0)

# hist_data = ts.get_h_data("510300", start='2017-01-01', end='2018-01-01')
# hist_data = ts.get_h_data("601857",start='2009-11-01',end='2010-01-01')
hist_data = ts.get_h_data("601857",start='2018-01-01')
hist_data.info()
print(hist_data)
exit(0)

data_list = []
for dates,row in hist_data.iterrows():
    t = date2num(dates)
    open,high,close,low = row[:4]
    datas = (t,open,high,low,close)
    data_list.append(datas)


fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()

plt.title("601857")
plt.xlabel("time")
plt.ylabel("price")

mpf.candlestick_ohlc(ax, data_list, width=1.5, colorup='r', colordown='green')

plt.grid()
plt.show()
print("\n")
