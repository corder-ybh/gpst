# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

#数据库
engine = create_engine('mysql://root:y20o8b93h2017@118.126.65.219/finance?charset=utf8')

#大单交易数据,可以获取当日的大单交易，价格，买卖盘等情况
#df = ts.get_sina_dd("000799",date='2018-07-13')

#print(df)

#当日历史交易分笔
#df = ts.get_today_ticks("000799", retry_count=3, pause=2)

#实时分笔
#df = ts.get_realtime_quotes('000799')

#历史分笔
#df = ts.get_tick_data('000799', date='2018-07-12', retry_count=6, pause=2)

#获取大盘指数
#df = ts.get_index()

#分配预案
#df = ts.profit_data(top=15, year=2018, retry_count=5, pause=3)

#业绩报告
#df = ts.forecast_data(2018,2)

#限售股解禁 (日期，数量（万股），占总盘比例)
#df = ts.xsg_data()

#基金持股(股票代码，股票名称，报告日期，基金家数，与上期相比clast，基金持股市值，占流通盘比例)
#df = ts.fund_holdings(2018, 1, retry_count= 9, pause= 8)

#沪市融资融券
#df = ts.sh_margins(start='2018-01-01', end='2018-03-01', retry_count=5, pause=4)

#沪市融资融券明细
#df = ts.sh_margin_details(start='2018-01-01', end='2018-05-01', symbol='000799')

#深市融资融券(信用交易日期，融资买入额(元)，融资余额(元)，融券卖出量，融券余量，融券余量(元)，融资融券余额(元))
#df = ts.sz_margins(start='2018-01-01', end='2018-03-01')

#深市融资融券明细数据(证券代码，证券简称，融资买入额，融资余额，融券卖出量，融券余量，融券余量(元))
#df = ts.sz_margin_details('2018-01-03')

#分类数据
#行业分类 (股票名称，行业名称)
#df = ts.get_industry_classified()

#概念分类
#df = ts.get_concept_classified()

#沪深300成分及权重
#df = ts.get_hs300s()

#上证50成分股
#df = ts.get_sz50s()

#终止上市股票列表 不能用了
#df = ts.get_terminated()

#暂停上市 也不能用了
#df = ts.get_suspended()

#基本面数据
#股票列表
df = ts.get_stock_basics()

#存款利率
#df = ts.get_deposit_rate()

#贷款利率（以上两个都太老了）
#df = ts.get_loan_rate()

#存款准备金率
#df = ts.get_rrr()

#货币供应量
#df = ts.get_money_supply()

#货币供应量 年底余额(没有17年的)
#df = ts.get_money_supply_bal()

#国内生产总值
#df = ts.get_gdp_year()

#国内生产总值 季度
#df = ts.get_gdp_quarter()

df.to_sql('tick_data', engine)
print(df)
#df.head(10)

