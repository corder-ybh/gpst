# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import datetime
import time
import math
import csv

# 获取均线数据
def xunpd(xpd) :
    global resultDf
    code = xpd['code']
    name = xpd['name']

    endDate = time.strftime("%Y-%m-%d", time.localtime())
    startDate = getnDayAgo(endDate, 100)

    dk = ts.get_k_data(code, start=startDate, end=endDate, retry_count=5,pause=2)

    # 计算均线
    days = [5, 34, 55, 50]
    for ma in days:
        column_name = "MA{}".format(ma)
        dk[column_name] = dk[['close']].rolling(window=ma).mean()

    opdf = dk.tail(10)

    #5日均线大小判断
    jx5 = 0
    for i in opdf.index :
        bar = opdf.loc[i]
        if (math.isnan(bar['MA5'])) :
            return
        elif (bar['MA5'] > bar['MA55']) :
            jx5 = jx5 + 1
            xpd['close'] = bar['close']
        else :
            jx5 = jx5 - 1

    print(xpd['index'])
    if jx5 > 5:
        xpd['jx5'] = jx5
        resultDf = resultDf.append(xpd, ignore_index=True)
        resultDf.to_csv("zhcx.csv", encoding='utf-8', index=False)
# 取多天前日期
def getnDayAgo(date, n) :
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

#csv 文件写入


#数据库
engine = create_engine('mysql://root:root@localhost:3306/finance?charset=utf8')
df = pd.read_sql_query("SELECT `index`, `name`,`code` FROM finance.stock_basics", con=engine)

resultDf = pd.DataFrame(columns = ["index", "name", "code", "close", "jx5"])

for i in df.index :
    xpd = df.loc[i]
    xunpd(xpd)

print(resultDf)
#for i in df.index :



