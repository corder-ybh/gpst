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

engine = create_engine('mysql://root:root@127.0.0.1:3306/finance?charset=utf8')
df = pd.read_sql(sql="SELECT `index`,`code`,`name`,`industry` FROM finance.stock_basics", con=engine)

# 获取n天前日期
def getNdatAgo(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]

def daywork(data) :
    code = data['code']

    # 获取数据将当日数据添加进
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = getNdatAgo(tDate, 1)
    caDf = pd.DataFrame()
    caDf = ts.get_k_data(code, end=tDate, retry_count=5, pause=2)
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
    caDf.to_sql('tick_data', engine,if_exists='append', index=False)


for i in df.index:
    daywork(df.loc[i])
    print(df.loc[i]['index'])
    if (i > 1000) :
        break