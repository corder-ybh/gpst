import tushare as ts
import numpy as np
import pandas as pd

#df = ts.get_sina_dd('000799',date='2018-06-29')
df = ts.profit_data(year=2018,top=60)
print df