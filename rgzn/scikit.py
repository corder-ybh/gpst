# -*- coding: UTF-8 -*-
import numpy as np
from sklearn import datasets

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

iris = datasets.load_iris()
#这个是鸢尾花数据集，总共150个数据集，花萼长度，花萼宽度，花瓣长度，花瓣宽度
# 用于区分山鸢尾花、变色鸢尾花、维吉尼亚鸢尾花
iris_x = iris.data #数据， 训练测试使用
iris_y = iris.target  #标签，监督验证学习 验证结果

#print(iris) #iris.data.shape
#将其可视化
print(iris.keys())

feature = iris['data']
print(feature.shape)

def plot_iris_projection(x_index, y_index):
    for t,marker,c in zip(xrange(3), ">ox", 'rgb'):
        plt.scatter(iris[target==t, x_index],
                    iris[target==t, y_index],
                    marker=marker, c=c)
        plt.xlabel(feature_names[x_index])
        plt.ylabel(feature_names[y_index]<br><br>parirs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])

for i, (x_index, y_index) in enumerate(pairs):
    plt.subplot(2,3,i)
    plot_iris_projection(x_index, y_index)
plt.show()

exit()





print(iris_x[0])

#拆分 训练数据和测试数据 安装0.7 0.3比例
x_train,x_test,y_train,y_test = train_test_split(iris_x, iris_y, test_size=0.3)
#print(y_train) 打乱测试数据
knn = KNeighborsClassifier()
knn.fit(x_train, y_train)
print(knn.predict(x_test) - y_test) #计算预测和目标的差
print("scope:", knn.score(x_train, y_train))