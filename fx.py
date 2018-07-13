# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt


def draw(code) :
    # 获取数据
    df = ts.get_k_data(code, start="2017-09-01")

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

    # 计算成交量
    df['xsVolume'] = df['volume'] / 100000 * 2 + 20

    # 打印图片
    df['5-50'] = 3 * df['5-50'] + 10
    df['jxd6'] = 3 * df['jxd6'] + 10
    df['jxd10'] = 3 * df['jxd10'] + 10

    df.index = pd.to_datetime(df.date)
    df[['close', 'MA5', 'MA34', 'MA55', '5-50', 'jxd6', 'jxd10', 'xsVolume']].plot()

    plt.grid(True, axis='y')
    plt.title(code)
    plt.show()

#候选
cad = ['600048','002507','603198','600463','600590','000519']
for code in cad :
    draw(code)

#0710 记录 600048可能要抄底了或者等金叉出现防止抄在半山腰，均线及k线均出现抬头趋势
#          002507卖点，应该要进入下跌趋势5日均线和55日均线要交叉了，上涨过程应该到头了
#          603198卖点，与上面类似
#          600463不明朗，下跌通道吧
#          600590不明朗，下跌通道吧
#          000519下跌趋势可能在收缩
