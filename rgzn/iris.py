# # -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris #导入数据集iris
from pandas.tools.plotting import radviz
from pandas.tools.plotting import andrews_curves
from pandas.tools.plotting import parallel_coordinates
from pandas.tools.plotting import scatter_matrix

#%matplotlib inline

# iris = load_iris()  #载入数据集
# print(iris.data) #打印输出
#共150条记录，分别代表50条山鸢尾 (Iris-setosa)、变色鸢尾(Iris-versicolor)、维吉尼亚鸢尾(Iris-virginica)
# print(iris.target)
# iris.data.hist()
# plt.show()

print("---------------------------")

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# sepal 花萼 petal 花瓣
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pd.read_csv(url, names=names)
# print(dataset)
print(dataset.describe())
# dataset.hist() #数据直方图histograms
# dataset.plot(x="sepal-length", y='sepal-width', kind='scatter') #scatter 散点图
# dataset.plot(kind='kde') #kde图
# dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False) #箱图
# radviz(dataset, 'class') #好像是散点图
# andrews_curves(dataset, 'class') #不知道啥图
# parallel_coordinates(dataset, 'class') #也不知道什么图
scatter_matrix(dataset, alpha=0.2, figsize=(6,6), diagonal='kde')

plt.show()

# from matplotlib import pyplot
# from sklearn.datasets import load_iris
#
# iris = load_iris()
# setosa_sepal_len = iris.data[:50, 0]
# setosa_sepal_width = iris.data[:50, 1]
#
# versi_sepal_len = iris.data[50:100, 0]
# versi_sepal_width = iris.data[50:100, 1]
#
# vergi_sepal_len = iris.data[100:, 0]
# vergi_sepal_width = iris.data[100:, 1]
#
# pyplot.scatter(setosa_sepal_len, setosa_sepal_width, marker = 'o', c = 'b',  s = 30, label = 'Setosa')
# pyplot.scatter(versi_sepal_len, versi_sepal_width, marker = 'o', c = 'r',  s = 50, label = 'Versicolour')
# pyplot.scatter(vergi_sepal_len, vergi_sepal_width, marker = 'o', c = 'y',  s = 35, label = 'Virginica')
# pyplot.xlabel("sepal length")
# pyplot.ylabel("sepal width")
# pyplot.title("sepal length and width scatter")
# pyplot.legend(loc = "upper right")
#
# pyplot.show()