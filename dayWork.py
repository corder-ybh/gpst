# -*- coding: UTF-8 -*-
'''
每日数据处理，需要每日将前一天的数据传入，然后循环检查一遍形式，并生成报表
'''
import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime
import time
import math
from configparser import ConfigParser

cf = ConfigParser()
cf.read('./gpst.conf')
dbHost = cf.get("db", "dbHost")
dbPort = cf.get("db", "dbPort")
dbUser = cf.get("db", "dbUser")
dbPass = cf.get("db", "dbPass")
dbName = cf.get("db", "dbName")

engine = create_engine(
    "mysql://" + dbUser + ":" + dbPass + "@" + dbHost + ":" + dbPort + "/" + dbName + "?charset=utf8")
conn = engine.connect()

df = pd.read_sql(sql="SELECT `index`,`code`,`name`,`industry` FROM finance.stock_basics", con=engine)

# 获取n天前日期
def getNdatAgo(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

def daywork(data) :
    global dbName
    code = data['code']

    # 获取数据将当日数据添加进
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 4)
    caDf = pd.DataFrame()
    caDf = ts.get_k_data(code, start=nDate, end=tDate, retry_count=5, pause=2)
    if (caDf is None or caDf.empty) :
        return
    print("get :{}".format(data['index']))
    # 计算浮动比例
    caDf["pchange"] = caDf.close.pct_change()
    # 计算浮动点数
    caDf["change"] = caDf.close.diff()
    # caDf['date'] = caDf.index
    caDf['code'] = code
    # caDf.reset_index(drop = True, inplace=True)
    date = caDf.iloc[-1]['date']
    sql = "SELECT 1 FROM " + dbName + ".tick_data WHERE code = '" + code + "' AND date = '"+date + "'"
    isExists = engine.execute(sql).fetchall()
    if (0 == len(isExists) or list(isExists[0])[0] != 1) :
        caDf = caDf.tail(2)
        caDf.to_sql('tick_data', engine,if_exists='append', index=False)
        print("insert :" + code)
    else :
        return



    #取该股票的数据进行分析，当前分析策略：排序检查出现5日均线雨55日均线交叉的，且55日均线是向上的，

    #取已买股票，计算成本

def analyStock(code) :

    # 获取数据
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 100)
    sql = "SELECT * FROM finance.tick_data WHERE code = '" + code + "' AND `date` > '" + nDate + "'"
    caDf = pd.read_sql(sql, con=engine)

    if (caDf is None or caDf.empty):
        return

    # 计算均线
    days = [5, 34, 55, 50]
    for ma in days:
        column_name = "MA{}".format(ma)
        caDf[column_name] = caDf[['close']].rolling(window=ma).mean()

    #10天之内5日均线与55日均线有交集
    # 计算55日均线浮动比例
    caDf["55pchange"] = caDf.MA55.pct_change()
    pChange55Sum = caDf.iloc[:,'55pchange'].sum()

    endDf = caDf.tail(10)
    feature = 0

    for i in endDf.index:
        temp = endDf.loc[i]
        newPrice = temp['close']
        if (math.isnan(temp['MA5'])):
            return
        elif (temp['MA5'] > temp['MA55']):
            feature += 1
        else:
            feature = 1

    if (feature > 6):
        head = endDf.iloc[1]
        tail = endDf.iloc[-1]

        if (head['MA5'] < head['MA55'] and tail['MA5'] > tail['MA55']):
            print(1)

#将数据保存为图片并发邮件


for i in df.index:
    daywork(df.loc[i])
    print(df.loc[i]['index'])