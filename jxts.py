# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt

data=ts.get_k_data("000725", start="2016-01-01", end="2017-01-01")    #选取600030股票

a = data.close
B = []
n = len(a)
for i in range(10, n):
    x5 = a[i-5:i].mean()                 #5日均线值
    x10 = a[i-10:i].mean()               #10日均线值
    B.append(x5 > x10)

o = data.open
m = len(B)
w = 0                   #利润

cash = 10000          #操作金额1亿，但考虑买的份额为100的整数，取1百万
amount = 0

PL = []              #利润w的数组
for i in range(1, m):
    k = i + 10
    if B[i-1] == 0 and B[i] == 1 and not amount:
        amount = cash // o[k]     #买入份额
        cash -= o[k] * amount
    elif B[i-1] == 1 and B[i]==0 and amount:
        cash += o[k] * amount      #卖出的金额
        amount = 0
#     print cash, amount

    PL.append(cash + o[k] * amount)

print("利润：{}".format(PL[-1]))


plt.plot(PL,color="green",label="Profit and Loss")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

plt.plot(a[10:], color="red",label="Profit and Loss")
plt.show()