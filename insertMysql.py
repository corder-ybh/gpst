# -*- coding: UTF-8 -*-
'''
用于将数据插入到数据库中
'''

import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime
import time
import math

engine = create_engine('mysql://root:root@localhost:3306/finance?charset=utf8')
df = pd.read_sql(sql="SELECT `index`,`code`,`name`,`industry` FROM finance.stock_basics", con=engine)


# 获取n天前日期
def getNdatAgo(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]


def insertInto(data):
    code = data['code']

    # 获取数据
    tDate = time.strftime("%Y-%m-%d", time.localtime())
    nDate = '2015-01-01'
    caDf = pd.DataFrame()
    caDf = ts.get_hist_data(code, start=nDate, end=tDate, retry_count=5, pause=2)
    if (caDf is None or caDf.empty) :
        return
    print("get :{}".format(data['index']))
    caDf['date'] = caDf.index
    caDf['code'] = code
    caDf.reset_index(drop = True, inplace=True)
    caDf.to_sql('tick_data', engine,if_exists='append')
    print("insert ok!")

for i in df.index:
    insertInto(df.loc[i])
    print(df.loc[i]['index'])
    if (i > 1000) :
        break

