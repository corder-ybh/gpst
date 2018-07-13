# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties
import matplotlib.dates as dt

from matplotlib.dates import DateFormatter
from mpl_finance import *

from datetime import timedelta, datetime

#获取数据
df = ts.get_k_data("600048", start="2017-09-01")
#df.index = pd.to_datetime(df.date)

#计算浮动比例
df["pchange"] = df.close.pct_change()
#计算浮动点数
df["change"] = df.close.diff()

#计算均线
days = [5, 34, 55, 50]
for ma in days:
  column_name = "MA{}".format(ma)
  df[column_name] = df[['close']].rolling(window=ma).mean()

#计算策略三所需参数
df['5-50'] = df['MA5'] - df['MA55']
df["pc5-50"] = df['5-50'].pct_change()
df['jxd6'] = df[['5-50']].rolling(window=6).mean()
df['jxd10'] = df[['5-50']].rolling(window=15).mean()

#计算成交量
df['xsVolume'] = df['volume'] / 100000 * 2 + 20

#设定回撤值
withdraw = 0.03
#设定突破值
breakthrough = 0.05
#设定账户资金
account = 10000
#持有仓位手数
position = 0
#上一次交易金额
cost = 0
#是否等待一天进行观察
isDelay = ''

#下单函数
def buy(bar):
  global account, position, cost
  print ("{}: buy {} position:{}".format(bar.date, bar.close, position))
  #一手价格
  one = bar.close * 100
  position = account //one
  account = account - (position * one)
  cost = bar.close
  
def sell(bar):
  global account, position, cost
  print ("{}: sell {} position:{} buy cost:".format(bar.date, bar.close, position, cost))
  #一手价格
  one = bar.close * 100
  account += position * one
  position = 0


#进行交易
print ("begin traction time:{}, begin money:{}".format(df.iloc[0].date, account))
for i in df.index:

  # 策略二、在均线的凹点买入，均线的凸点卖出，不好用！
  # if ( i < 6) :
  #     continue
  # bar = df.loc[i]
  # yesBar = df.loc[i-1]
  # bfBar = df.loc[i-2]
  #
  # nowAccount = account + position * df.iloc[i-1].close * 100

  # if (nowAccount < 10000 * (1 - withdraw)) :
  #   #跌幅达回撤值时回撤
  #   print("withdraw at {}".format(nowAccount / 10000))
  #   sell(bar)
  # if (bfBar['MA3'] > yesBar['MA3'] and yesBar['MA3'] < bar['MA3'] and not position):
  #   buy(bar)
  # if (bfBar['MA3'] < yesBar['MA3'] and yesBar['MA3'] > bar['MA3'] and position):
  #   #减小低卖的情况
  #   if (bar['close'] > cost):
  #     sell(bar)

  # #策略一金叉买入，死叉卖出
  # bar = df.loc[i]
  # if (i == 0):
  #   continue
  # yesMA5 = df.loc[i-1].MA5
  # yesMA50 = df.loc[i-1].MA50
  # nowMA5 = bar['MA5']
  # nowMA50 = bar['MA50']
  # if (yesMA5 < yesMA50 and nowMA5 > nowMA50):
  #   #金叉买入
  #   buy(bar)
  # if (yesMA5 > yesMA50 and nowMA5 < nowMA50) :
  #   #死叉卖出
  #   sell(bar)

  #策略三 使用均线之间距离进行判断，如果均线间距离拉大，而均线还在下行，那么均线到底时买入，均线到顶时买入
  if (i < 165) :
    continue
  bar = df.loc[i]
  yesBar = df.loc[i-1]
  bfBar = df.loc[i-2]
  tf = abs((yesBar['5-50'] - (bfBar['5-50'] + yesBar['5-50'] + bar['5-50']) / 3) / yesBar['5-50'])
  #寻找买入机会，寻底过程
  if (yesBar['MA5'] < yesBar['MA55'] and bar['MA5'] > bar['MA55'] and not position) :
    zf = (bar['close'] - bar['MA55']) / bar['close']
    if (isDelay == "w1") :
      #处理前两天出现买点，但是幅度不正常，观察一天
      if (bar['pchange'] < 0) :
        #买点出现后第二天就下跌，那么跳过此买点
        print("tiaoguo pc:{}".format(bar['pchange']))
        isDelay = ""
        continue
    #如果振幅异常，那么观察一天再买入
    if (zf > 0.03) :
      isDelay = "w1"
      continue
    print("sell bf:{} yes:{} td:{} 5-50pc:{} tf:{} zf:{} pc:{}".format(bfBar['5-50'], yesBar['5-50'], bar['5-50'], bar['pc5-50'], tf, zf,bar['pchange']))
    buy(bar)



  #寻找卖出机会，防止过早卖出，容易被洗盘洗出去
  if (bfBar['jxd6'] < yesBar['jxd6'] and yesBar['jxd6'] > bar['jxd6'] and position) :
    print("sell bf:{} yes:{} td:{} 5-50pc:{} tf:{}".format(bfBar['jxd6'], yesBar['jxd6'], bar['jxd6'], bar['pc5-50'], tf))
    sell(bar)

print("finally cash:", account)
print("finally market values:", position * df.iloc[-1].close * 100)

#打印图片
df['5-50'] = 3 * df['5-50'] + 10
df['jxd6'] = 3 * df['jxd6'] + 10
df['jxd10'] = 3 * df['jxd10'] + 10

df.index = pd.to_datetime(df.date)
df[['close','MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10']].plot()

'''
plt.plot(df[['close','MA5','MA50','xsVolume']])
plt.title('junxian xitong')
plt.xlabel('date')

'''
plt.grid(True,axis='y')
plt.show()
