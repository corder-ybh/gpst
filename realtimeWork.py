# -*- coding: UTF-8 -*-
'''
实时数据处理，需要每日将前一天的数据传入，然后循环检查一遍形式，并生成报表
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

positionDf = pd.read_sql(sql="SELECT `code`, `buy_price`, `tips_num`, `tips_time` FROM finance.position", con=engine)
resultLost = list()
resultEarn = list()

'''
更新提醒次数
'''
def updateTips(code, num):
    sql = "UPDATE finance.position set tips_num = tips_num + "+str(num)+", tips_time = NOW() WHERE `code` = '"+str(code)+"'"
    engine.execute(sql)


def realAnalysis(temp):
    global result

    code = temp['code']
    # 获取数据

tRealData = ts.get_realtime_quotes(positionDf['code'])
tRealData.set_index('code', inplace=True)
for i in positionDf.index:
    temp = positionDf.loc[i]

    code = temp['code']
    buyPrice = temp['buy_price']
    tipsNum = temp['tips_num']
    tipsTime = temp['tips_time']

    nowDataSe = tRealData.loc[code]
    nowPrice = float(nowDataSe['price'])

    updateTips(code, 1)
    profit = nowPrice / buyPrice

    #一级提醒
    if (profit <= 0.97):
        #已报警则跳过
        if (tipsNum <= -1):
            #是否达到2级报警
            if (profit <= 0.96 and tipsNum >= 2):
                #进行报警
                resultLost.append(code)
                updateTips(code, -1)
            else:
                continue
        resultLost.append(code)
    if (profit > 1.03):
        resultEarn.append(code)
    print(i)


strTo = [email]
strFrom = 'root@us-west-2.compute.internal'
eh = EmailHandler()
tDate = time.strftime("%Y-%m-%d", time.localtime())


eh.sendPicMail(strTo, title, tempJc)
