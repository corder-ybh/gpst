# -*- coding: UTF-8 -*-
# import matplotlib as mpl
# mpl.use('Agg')

import time
import datetime
from sqlalchemy import create_engine
from configparser import ConfigParser
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts


import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入

sys.setdefaultencoding('utf-8')

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
    nDate = getNdatAgo(tDate, 365)
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
    plt.savefig('./img/'+code +'.png')

    df = df.tail(50)
    df[['close', 'MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10', 'xsVolume']].plot()
    plt.grid(True, axis='y')
    plt.title(code + "-latest")
    plt.savefig('./img/'+code + '-latest.png')
    plt.close('all')

#获取股票的基本数据
def getTickInfo(code):
    sql = "SELECT * FROM finance.stock_basics tk WHERE tk.`code` = '" + code + "'"
    resDf = pd.read_sql(sql, con=engine)
    resSe = resDf.iloc[0]
    resStr = "code:"+str(resSe['code'])+" name:"+str(resSe['name'])+" industry:"+str(resSe['industry'])+"上市日期"+str(resSe['timeToMarket'])\
             +" 地区:" +str(resSe['area'])+" 市盈率:"+str(resSe['pe']) + " 流通股本(亿):"+str(resSe['outstanding'])+" 总股本(亿):"+str(resSe['totals']) \
             +" 总资产(万):"+str(resSe['totalAssets'])+" 流动资产:"+str(resSe['liquidAssets'])+" 固定资产:"+str(resSe['fixedAssets']) +" 公积金:"+str(resSe['reserved'])\
             +" 每股公积金:"+str(resSe['reservedPerShare'])+" 每股收益:"+str(resSe['esp'])+" 每股净资:"+str(resSe['bvps']) +" 市净率:"+str(resSe['pb'])\
             +" 未分利润:"+str(resSe['undp'])+" 每股未分配:"+str(resSe['perundp'])+" 收入同比(%):"+str(resSe['rev']) +" 利润同比(%):"\
             +str(resSe['profit'])+" 毛利率(%):"+str(resSe['gpr'])+" 净利润率(%):"+str(resSe['npr'])+" 当前股东人数"+str(resSe['holders'])
    return  resStr

#更新股票基本信息，并记录日志
def updateStock():
    sbDf = ts.get_stock_basics()
    for index in  sbDf.index:
        temp = sbDf.loc[index]
        code = index
        tDate = time.strftime("%Y-%m-%d", time.localtime()) #今日日期

        checkSql = "SELECT 1 FROM finance.stock_his WHERE `code`='"+code+"' AND `date`='"+tDate+"'"
        isExists = engine.execute(checkSql).fetchall()
        if (0 == len(isExists) or list(isExists[0])[0] != 1):
            # 如果无今日数据那么先把今日的数据保存下来
            sql = "SELECT `code`,`pe`,`pb`,`holders` FROM finance.stock_basics WHERE `code` = '" + code + "'"
            hisDf = pd.read_sql(sql, con=engine)
            hisDf['date'] = tDate
            hisDf.to_sql('stock_his', engine, if_exists='append', index=False)
        insertSql = "INSERT INTO `finance`.`stock_basics`" \
                    "(`name`, `industry`, `area`, `pe`, `outstanding`, `totals`, `totalAssets`, `liquidAssets`, " \
                    "`fixedAssets`,`reserved`, `reservedPerShare`, `esp`, `bvps`, `pb`, `timeToMarket`, `undp`," \
                    " `perundp`, `rev`, `profit`,`gpr`, `npr`, `holders`, `code`) " \
                    "VALUES " \
                    "('"+str(temp['name'])+"', '"+str(temp['industry'])+"', '"+str(temp['area'])+"', '"+str(temp['pe'])+"', '"+str(temp['outstanding'])+\
                    "', '"+str(temp['totals'])+"', '"+str(temp['totalAssets'])+"', '"+str(temp['liquidAssets'])+"', '"+str(temp['fixedAssets'])+\
                    "','"+str(temp['reserved'])+"', '"+str(temp['reservedPerShare'])+"', '"+str(temp['esp'])+"', '"+str(temp['bvps'])+"', '"+ \
                    str(temp['pb'])+"', '"+str(temp['timeToMarket'])+"', '"+str(temp['undp'])+"', '"+str(temp['perundp'])+"', '"+str(temp['rev'])+"', '"+str(temp['profit'])+\
                    "','"+str(temp['gpr'])+"', '"+str(temp['npr'])+"', '"+str(temp['holders'])+"','"+str(code)+"') ON DUPLICATE KEY UPDATE `name` = VALUES(`name`),`industry`=VALUES(`industry`), `area`=VALUES(`area`), `pe`=VALUES(`pe`), `outstanding`=VALUES(`outstanding`), `totals`=VALUES(`totals`),  `totalAssets`=VALUES(`totalAssets`),`liquidAssets`=VALUES(`liquidAssets`), `fixedAssets`=VALUES(`fixedAssets`), `reserved`=VALUES(`reserved`), `reservedPerShare`=VALUES(`reservedPerShare`), `esp`=VALUES(`esp`),`bvps`=VALUES(`bvps`), `pb`=VALUES(`pb`), `timeToMarket`=VALUES(`timeToMarket`), `undp`=VALUES(`undp`), `perundp`=VALUES(`perundp`), `rev`=VALUES(`rev`),  `profit`=VALUES(`profit`), `gpr`=VALUES(`gpr`), `npr`=VALUES(`npr`), `holders`=VALUES(`holders`)"
        engine.execute(insertSql)
        print("updateStock:"+index)

