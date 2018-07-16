# -*- coding: UTF-8 -*-

import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime
import time
import math

engine = create_engine('mysql://root:root@localhost:3306/finance?charset=utf8')
df = pd.read_sql(sql="SELECT `index`,`code`,`name`,`industry` FROM finance.stock_basics", con=engine)

#获取n天前日期
def getNdatAgo(date, n) :
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

def calAvePrice(data) :
    code = data['code']
    index = data['index']
    name = data['name']
    industry = data['industry']

    #获取数据
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 100)
    caDf = ts.get_k_data(code, start=nDate, end=tDate, retry_count=5,pause=2)

    if (caDf is None or caDf.empty) :
        return

    #计算均线
    days = [5, 34, 55, 50]
    for ma in days:
        column_name = "MA{}".format(ma)
        caDf[column_name] = caDf[['close']].rolling(window=ma).mean()

    endDf = caDf.tail(10)
    feature = 0
    newPrice = 0

    for i in endDf.index :
        temp = endDf.loc[i]
        newPrice = temp['close']
        if (math.isnan(temp['MA5'])) :
            return
        elif (temp['MA5'] > temp['MA55']) :
            feature += 1
        else :
            feature = 1

    if (feature > 6) :
        head = endDf.iloc[1]
        tail = endDf.iloc[-1]

        if(head['MA5'] < head['MA55'] and tail['MA5'] > tail['MA55']) :
            res = pd.DataFrame({"index":index,"code":code, "name":name,"industry":industry, "newPrice":newPrice},index=["0"])
            res.to_csv("res.csv",index=0, encoding='utf8', sep=',', mode='a', header=0)

#筛选股价在55日均线下的股票
def under55jx(data) :
    code = data['code']
    index = data['index']
    name = data['name']
    industry = data['industry']

    # 获取数据
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 700)
    caDf = ts.get_k_data(code, start=nDate, end=tDate, retry_count=5, pause=2)

    if (caDf is None or caDf.empty) :
        return
    days = [5, 34, 55, 50]

    for ma in days:
        column_name = "MA{}".format(ma)
        caDf[column_name] = caDf[['close']].rolling(window=ma).mean()

    # 计算浮动比例
    caDf["pcMA55"] = caDf.MA55.pct_change()

    sum = caDf.pcMA55.sum()
    print(sum)

for i in df.index :
    # if (i < 1970) :
    #     continue
    under55jx(df.loc[10])
    print(df.loc[i]['index'])

