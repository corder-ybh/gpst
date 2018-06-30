# -*- coding: UTF-8 -*-

import tushare as ts
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

print(ts.__version__)
'''
df1 = ts.get_k_data('000001',ktype='D',start='2015-01-01',end='2015-01-31')
print df1.shape
print df1
df2 = ts.get_k_data('000002',ktype='D',start='2015-01-01',end='2015-01-31')
print 'all:'
result = [df1,df2]
df = pd.concat(result)
print df
print 'get all'
print df.iloc[1:4][:]
print 'get jun zhi'
print df[df]
'''

stock_list = ['000001', '000002', '000568', '000625', '000768', '600028', '600030', '601111', '601390', '601998']
i = 0
print 'option'
for index in stock_list:
  df = ts.get_k_data(index,ktype='D',start='2015-01-01',end='2015-01-31',autype='none')
  if i == 0 :
    frame = df
  else :
    frame = [frame,df]
    frame = pd.concat(frame)
  i = i + 1;
df = frame
df.index = range(len(df))
print "Order by column value, ascending:"
print df.sort_values('date').head()
print "Order by multiple column value:"
df = df.sort_values(['date','code'], ascending=[False,True])
print df.head()
print 'shoupanjia > mean'
print df[df.close > df.close.mean()].head()
print 'guolv'
print df[df['code'].isin(['000001','0000002'])].head()
print df.shape
df = frame[['date','code','volume','open','close','high','low','close']]
print df
print df.mean(0)
#print df['close'].value_counts().head()
print df[['close']].apply(lambda x: (x - x.min()) / (x.max() - x.min())).head()
print 'dat1'
dat1 = df[['code','date','close']].head()
dat2 = df[['code','date','close']].iloc[2]
print "Before appending"
print dat1
dat = dat1.append(dat2,ignore_index=True)
print "After appending"
print dat

print "hebing"
dat1 = df[['code','date','close']]
dat2 = df[['code','date','volume']]
dat = dat1.merge(dat2, on=['code','date'])
print "first dataframe"
print dat1.head()
print "second dataframe"
print dat2.head()
print "merged dataframe"
print dat.head()

print 'group by'
df_grp = df.groupby('code')
grp_mean = df_grp.mean()
print grp_mean

df2 = df.sort_values(['code','date'], ascending=[True, False])
#print df2.drop_duplicates(subset='code')
print df2.drop_duplicates(subset='code', keep='last')
print 'huitu'
dat = df[df['code'] == '600028'].set_index('date')['close']
print dat
plt.plot(dat)
plt.title('600028 close 2015-01')
plt.xlabel('date')
plt.ylabel('close')
#plt.show()

dates = pd.date_range('20150101', periods=5)
print dates

df = pd.DataFrame(np.random.randn(5,4),index=dates,column=list('ABCD))
print df

