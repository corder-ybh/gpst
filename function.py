# -*- coding: UTF-8 -*-
# import matplotlib as mpl
# mpl.use('Agg')

import time
import datetime
from sqlalchemy import create_engine
from configparser import ConfigParser
import pandas as pd
import matplotlib.pyplot as plt

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

# 获取n天前日期
def getNdatAgo(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

def draw(code) :
    # 获取数据
    # df = ts.get_k_data(code, start="2017-09-01")
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 100)
    sql = "SELECT * FROM finance.tick_data WHERE code = '" + code + "' AND `date` > '" + nDate + "'"
    df = pd.read_sql(sql, con=engine)

    # 计算浮动比例
    df["pchange"] = df.close.pct_change()
    # 计算浮动点数
    df["change"] = df.close.diff()

    # 计算均线
    days = [5, 34, 55, 50]
    for ma in days:
        column_name = "MA{}".format(ma)
        df[column_name] = df[['close']].rolling(window=ma).mean()

    # 计算策略三所需参数
    df['5-50'] = df['MA5'] - df['MA55']
    df["pc5-50"] = df['5-50'].pct_change()
    df['jxd6'] = df[['5-50']].rolling(window=6).mean()
    df['jxd10'] = df[['5-50']].rolling(window=15).mean()

    #基数确定
    baseNum = df['MA55'].min()

    # 计算成交量
    df['xsVolume'] = df['volume'] / 100000 * 2 + baseNum + 3

    # 打印图片
    df['5-50'] = 3 * df['5-50'] + baseNum - 3
    df['jxd6'] = 3 * df['jxd6'] + baseNum - 3
    df['jxd10'] = 3 * df['jxd10'] + baseNum - 3

    df.index = pd.to_datetime(df.date)

    df[['close', 'MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10', 'xsVolume']].plot()

    plt.grid(True, axis='y')
    plt.title(code)
    plt.savefig(code +'.png')

    df = df.tail(50)
    df[['close', 'MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10', 'xsVolume']].plot()
    plt.grid(True, axis='y')
    plt.title(code + "-latest")
    plt.savefig(code + '-latest.png')
