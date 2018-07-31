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
from sendPic import EmailHandler

cf = ConfigParser()
cf.read('./gpst.conf')
dbHost = cf.get("db", "dbHost")
dbPort = cf.get("db", "dbPort")
dbUser = cf.get("db", "dbUser")
dbPass = cf.get("db", "dbPass")
dbName = cf.get("db", "dbName")
email = cf.get("base", "email")

engine = create_engine(
    "mysql://" + dbUser + ":" + dbPass + "@" + dbHost + ":" + dbPort + "/" + dbName + "?charset=utf8")
conn = engine.connect()

df = pd.read_sql(sql="SELECT `index`,`code`,`name`,`industry` FROM finance.stock_basics", con=engine)
resultJc = list()
result55 = list()


# 获取n天前日期
def getNdatAgo(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

def analyStock(code):
    global result

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

    # 10天之内5日均线与55日均线有交集
    # 计算55日均线浮动比例
    caDf["55pchange"] = caDf.MA55.pct_change()

    endDf = caDf.tail(6)
    endDf.reset_index(drop=True, inplace=True)
    feature = 0
    # 首末项
    head = endDf.iloc[0]
    tail = endDf.iloc[-1]

    # for i in endDf.index:
    #     temp = endDf.loc[i]
    #
    #     if (math.isnan(temp['MA5'])):
    #         return
    #     elif (temp['MA5'] > temp['MA55']):
    #         feature += 1
    #     else:
    #         feature = feature - 1
    #
    # if (feature > 5):
    # 6天之内有均线金叉出现，5日均线上穿55日均线
    if (head['MA5'] < head['MA55'] and tail['MA5'] > tail['MA55']):
        # 进行发送处理
        resultJc.append(code)
        print("jc:" + code)

    # 是否低于55日均线
    end5Df = caDf.tail(6)
    isLow55 = 0
    isUp = 0
    for i in end5Df.index:
        temp = end5Df.loc[i]

        tClose = temp['close']
        t55MA = temp['MA55']
        tPChange = temp['pchange']

        #5日以内低于55日均线的
        if (tClose < t55MA):
            isLow55 = isLow55 + 1
        else:
            isLow55 = isLow55 - 1

        if (tPChange > 0):
            isUp = isUp + 1
        else:
            isUp = isUp - 1

    #6日以内有4日以上是低于55日线，且有3日以上是上涨状态
    if (isLow55 > 4 and isUp > 3):
        result55.append(code)
        print ("55:" + code)
'''
20日短期均线分析
'''
def analyStockShort(code):
    global result

    # 获取数据
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 70)
    sql = "SELECT * FROM finance.tick_data WHERE code = '" + code + "' AND `date` > '" + nDate + "'"
    caDf = pd.read_sql(sql, con=engine)

    if (caDf is None or caDf.empty):
        return

    # 计算均线
    days = [5, 10, 20, 30]
    for ma in days:
        column_name = "MA{}".format(ma)
        caDf[column_name] = caDf[['close']].rolling(window=ma).mean()

    # 计算20日均线浮动比例
    caDf["20pchange"] = caDf.MA20.pct_change()

    endDf = caDf.tail(2)
    endDf.reset_index(drop=True, inplace=True)

    # 首末项
    head = endDf.iloc[0]
    tail = endDf.iloc[-1]

    # 2天之内有均线金叉出现，5日均线上穿20日均线
    head5 = head['MA5']
    head20 = head['MA20']
    tail5 = tail['MA5']
    tail20 = tail['MA20']
    if (head['MA5'] < head['MA20'] and tail['MA5'] > tail['MA20']):
        # 进行发送处理
        resultJc.append(code)
        print("jc:" + code)




for i in df.index: #df.index
    temp = df.loc[i]
    code = temp['code']
    #每日添加和分析，两个函数开启一个即可
    analyStockShort(code)
    print(df.loc[i]['index'])
# # #result = ['002770', '002164']
strTo = [email]
strFrom = 'root@us-west-2.compute.internal'
eh = EmailHandler()
tDate = time.strftime("%Y-%m-%d", time.localtime())

# resultJc = ['002770','002164']

tempJc = list()
cs = math.ceil(float(len(resultJc)) / 10)
for i in range(0, int(cs)):
    tempJc = resultJc[(i*10):(i+1)*10]
    title = tDate + "-JC报表" + str(i)
    time.sleep(1)
    print("jc:"+str(i))
    eh.sendPicMail(strTo, title, tempJc)

temp55 = list()
cs = math.ceil(float(len(result55)) / 10)
for i in range(0, int(cs)):
    temp55 = result55[(i*10):(i+1)*10]
    title = tDate + "-55报表" + str(i)
    time.sleep(1)
    print("55:"+str(i))
    eh.sendPicMail(strTo, title, temp55)
