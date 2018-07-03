# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as dt

from matplotlib.dates import DateFormatter
from mpl_finance import *

from datetime import timedelta, datetime

#获取数据
df = ts.get_k_data("000799", start="2017-01-01", end="2018-01-01")
#df.index = pd.to_datetime(df.date)

#计算浮动比例
df["pchange"] = df.close.pct_change()
#计算浮动点数
df["change"] = df.close.diff()

#计算均线
days = [5, 15, 50]
for ma in days:
  column_name = "MA{}".format(ma)
  df[column_name] = df[['close']].rolling(window=ma).mean()

#设定回撤值
withdraw = 0.04
#设定突破值
breakthrough = 0.05
#设定账户资金
account = 10000
#持有仓位手数
position = 0

#下单函数
def buy(bar):
  global account, position
  print ("{}: buy {} position:{}".format(bar.date, bar.close, position))
  #一手价格
  one = bar.close * 100
  position = account //one
  account = account - (position * one)
  
def sell(bar):
  global account, position
  print ("{}: sell {} position:{}".format(bar.date, bar.close, position))
  #一手价格
  one = bar.close * 100
  account += position * one
  position = 0
  
#进行交易
print ("begin traction time:{}, begin money:{}".format(df.iloc[0].date, account))
for i in df.index:
  bar = df.loc[i]
  if (i == 0):
    continue
  yesMA5 = df.loc[i-1].MA5
  yesMA50 = df.loc[i-1].MA50
  nowMA5 = bar['MA5']
  nowMA50 = bar['MA50']
  if (nowMA5 > nowMA50):
    #金叉买入
    if bar.pchange and bar.pchange > breakthrough and position == 0:
      buy(bar)
    elif bar.pchange and bar.pchange < withdraw and position > 0:
      sell(bar)
  if (yesMA5 > yesMA50 and nowMA5 < nowMA50 and position) :
    #死叉卖出
    sell(bar)

print("finally cash:", account)
print("finally market values:", position * df.iloc[-1].close * 100)

#打印图片
df.index = pd.to_datetime(df.date)
df[['close','MA5','MA50']].plot()
'''
plt.plot(df[['close','MA5','MA50']])
plt.title('junxian xitong')
plt.xlabel('date')
'''
plt.show()
