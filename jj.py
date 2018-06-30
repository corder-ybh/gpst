# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt

df = ts.get_k_data("000799", start="2018-01-01", end="2018-06-29")

print (df.head())
print (df.tail())
df.index = pd.to_datetime(df.date)
df.drop("date", inplace=True, axis=1)
print (df.tail())
days = [5, 15, 50]
for ma in days:
  column_name = "MA{}".format(ma)
  df[column_name] = df[['close']].rolling(window=ma).mean()
df["pchange"] = df.close.pct_change()
df["change"] = df.close.diff()

print (df.tail(6))

df[['close','MA5','MA15','MA50']].plot()
plt.plot(df[['close','MA5','MA15','MA50']])
plt.title('600028 close 2015-01')
plt.xlabel('date')
plt.show()
'''
import pandas as pd
import numpy as np
from pandas import *

print (pd.__version__)
df = pd.DataFrame({'key1':['a','a','b','b','a'],
               'key2':['one','two','one','two','one'],
               'data1':np.nan,
               'data2':np.random.randn(5)})
print df
df['mean'] = df[['data2']].rolling(window=3).mean()
print df
'''  