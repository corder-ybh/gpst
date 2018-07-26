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


def daywork(data):
    global dbName
    code = data['code']

    # 获取数据将当日数据添加进
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 4)
    caDf = pd.DataFrame()
    caDf = ts.get_k_data(code, start=nDate, end=tDate, retry_count=5, pause=2)
    if (caDf is None or caDf.empty):
        return
    # 计算浮动比例
    caDf["pchange"] = caDf.close.pct_change()
    # 计算浮动点数
    caDf["change"] = caDf.close.diff()
    # caDf['date'] = caDf.index
    caDf['code'] = code
    # caDf.reset_index(drop = True, inplace=True)
    date = caDf.iloc[-1]['date']
    sql = "SELECT 1 FROM " + dbName + ".tick_data WHERE code = '" + code + "' AND date = '" + date + "'"
    isExists = engine.execute(sql).fetchall()
    if (0 == len(isExists) or list(isExists[0])[0] != 1):
        caDf = caDf.tail(2)
        caDf.to_sql('tick_data', engine, if_exists='append', index=False)
        print("insert :" + code)
    else:
        return



    # 取该股票的数据进行分析，当前分析策略：排序检查出现5日均线雨55日均线交叉的，且55日均线是向上的，

    # 取已买股票，计算成本


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

    endDf = caDf.tail(8)
    feature = 0
    # 首末项
    head = endDf.iloc[1]
    tail = endDf.iloc[-1]

    for i in endDf.index:
        temp = endDf.loc[i]

        if (math.isnan(temp['MA5'])):
            return
        elif (temp['MA5'] > temp['MA55']):
            feature += 1
        else:
            feature = feature - 1

    if (feature > 5):
        # 10天之内有均线金叉出现，5日均线上穿55日均线
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


# 将数据保存为图片并发邮件



for i in df.index: #df.index
    temp = df.loc[i]
    code = temp['code']
    #每日添加和分析，两个函数开启一个即可
    #daywork(df.loc[i])
    analyStock(code)
    print(df.loc[i]['index'])
# #result = ['000799', '600183']
strTo = [email]
strFrom = 'root@us-west-2.compute.internal'
eh = EmailHandler()
tDate = time.strftime("%Y-%m-%d", time.localtime())

# resultJc = ['000799', '600183','000791', '600182','000793', '600184','000795', '600186','000797', '600188','000799', '600181'
#           ,'000712','612183', '002391', '230182', '023793', '643184', '475795', '643186', '246797', '600188', '000799', '600181'
#     , '123344', '231533', '214356', '213435', '326534', '214355', '243556', '231545', '246797', '600188', '000799',
#           '600181']

tempJc = list()
cs = math.ceil(float(len(resultJc)) / 10)
for i in range(0, int(cs)):
    tempJc = resultJc[(i*10):(i+1)*10]
    title = tDate + "-JC报表" + str(i)
    eh.sendPicMail(strTo, title, tempJc)

temp55 = list()
cs = math.ceil(float(len(result55)) / 10)
for i in range(0, int(cs)):
    temp55 = result55[(i*10):(i+1)*10]
    title = tDate + "-55报表" + str(i)
    eh.sendPicMail(strTo, title, temp55)
