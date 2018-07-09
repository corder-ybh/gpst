# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from matplotlib.dates import DateFormatter
from mpl_finance import *

#可把我牛逼坏了
def candlePlot(data, title=''):
  data["date"] = [dt.date2num(pd.to_datetime(x)) for x in data.index]
  print data
  dataList = [tuple(x) for x in data[
    ["date", "open", "high", "low", "close"]].values]
	
  ax = plt.subplot()
  ax.set_title(title)
  ax.xaxis.set_major_formatter(DateFormatter("%y-%m-%d"))
  candlestick_ohlc(ax, dataList, width=0.7, colorup="r", colordown="g")
  plt.setp(plt.gca().get_xticklabels(), rotation=50,
    horizontalalignment="center")
  fig = plt.gcf()
  fig.set_size_inches(20, 15)
  plt.grid(True)
  #plt.show()
 
df = ts.get_k_data("603198", start="2017-07-01", end="2017-08-29")
df.index = pd.to_datetime(df.date)
df.drop("date", inplace=True, axis=1)
candlePlot(df)