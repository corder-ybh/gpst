# -*- coding: UTF-8 -*-

#导入相关模块
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from matplotlib.dates import DateFormatter
from mpl_finance import *


#获取数据
df = ts.get_k_data("000725", start="2016-01-01", end="2018-12-31")
df.index = pd.to_datetime(df.date)
#df.drop("date", inplace=True, axis=1)

#计算浮动比例
df["pchange"] = df.close.pct_change()
#计算浮动点数
df['change'] = df.close.diff()

#print df.head()

#设定回撤值
withdraw = 0.03
#设定突破值
breakthrough = 0.05
#设定账户资金
account = 10000
#持有仓位手数
position = 0

def buy(bar):
  global account, position
  print ("{}: buy {} position:{}".format(bar.date, bar.close, position))
  #一手价格
  one = bar.close * 100
  position = account //one
  account = account - (position * one)
 
def sell(bar):
  global account, position
  #一手价格
  print ("{}:sell {} posstion:{}".format(bar.date, bar.close, position))
  one = bar.close * 100
  account += position * one
  position = 0
  
print ("begin traction time:{}, begin money:{}".format(df.iloc[0].date, account))
for date in df.index:
  bar = df.loc[date]
  if bar.pchange and bar.pchange > breakthrough and position == 0:
    buy(bar)
  elif bar.pchange and bar.pchange < withdraw and position > 0:
    sell(bar)

print("finally cash:", account)
print("finally market values:", position * df.iloc[-1].close * 100)
