# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import time
import matplotlib.pyplot as plt
from function import getNdatAgo
from sqlalchemy import create_engine
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

    df = df.tail(70)
    df[['close', 'MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10', 'xsVolume']].plot()
    plt.grid(True, axis='y')
    plt.title(code + "-latest")
    plt.savefig(code + '-latest.png')


#候选
#cad = []
cad = ['603606','300451','300523','002458']
for code in cad :
    draw(code)

#0710 记录 600048可能要抄底了或者等金叉出现防止抄在半山腰，均线及k线均出现抬头趋势
#          002507卖点，应该要进入下跌趋势5日均线和55日均线要交叉了，上涨过程应该到头了
#          603198卖点，与上面类似
#          600463不明朗，下跌通道吧
#          600590不明朗，下跌通道吧
#          000519下跌趋势可能在收缩
#300132 已经涨了一波了
#603228 没有量，但是在上涨
#300559 已经在高位了，但是不知道为什么会上涨，生物制药类，可能会受华大影响
#300529 股价已经拉高
#002039 没点动静。均线长期向下
#600131 55日均线趋势向下，5日均线升势放缓
#300042 一直跌，股价围绕55日均线纠缠，但是55日均线一直向下
#000990 一直跌，不考虑了，55日均线趋势一直向下，股价长期低于55日均线，拉低55日均线
#002007 可能再来一个小高峰，错过了最佳买卖时机
#600789 可能是个机会
#600246 5块钱，毫无波动，pass
#600132 跌入到谷底刚出来，可能可以考虑下，不过已经被拉的比较高了
#603096 不推荐涨跌较大，看下基本面吧
#300517 涨势放缓 不考虑，可能要进入下降趋势了
#600183 长期看跌，短线向上 ok
#300365 长期看波动较大，刚从55日均线上来，可以考虑下
#600240 与均线长期纠缠，波动不大，涨跌幅较小
#002179 已经涨了一波了也许可以考虑


