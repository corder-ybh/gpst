# # -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

hua = load_iris()

########################################线性回归预测###################
# #获取花瓣的长和宽
# x = [n[0] for n in hua.data]
# y = [n[1] for n in hua.data]
#
# #由于x和y都为list类型，而使用线性回归fit()函数训练时，需要转换未数组array类型
# x = np.array(x).reshape(len(x), 1)
# y = np.array(y).reshape(len(y), 1)

# 导入sklearn机器学习拓展包中线性回归模型，然后进行训练和预测
# clf = LinearRegression()
# clf.fit(x, y)
# pre = clf.predict(x)
#
# #调用Matplotlib扩展包并绘制相关图形
# import matplotlib.pyplot as plt
# plt.scatter(x,y,s=100)
# plt.plot(x,pre,"r-", linewidth=4)
# for idx, m in enumerate(x):
#     plt.plot([m,m], [y[idx], pre[idx]], 'g-')
# plt.show()
########################################线性回归预测###################

########################################决策树分析###################
from sklearn.tree import DecisionTreeClassifier

# 训练集
train_data = np.concatenate((hua.data[0:40, :], hua.data[50:90, :], hua.data[100:140, :]), axis = 0)
train_target = np.concatenate((hua.target[0:40], hua.target[50:90], hua.target[100:140]), axis = 0)
#测试集
test_data = np.concatenate((hua.data[40:50, :], hua.data[90:100, :], hua.data[140:150, :]), axis = 0)
test_target = np.concatenate((hua.target[40:50], hua.target[90:100], hua.target[140:150]), axis = 0)


#训练
clf = DecisionTreeClassifier()
clf.fit(train_data, train_target)
predict_target = clf.predict(test_data)
print(predict_target)

#预测结果与真实结果比对
print(sum(predict_target == test_target))

#输出准确率 召回率 F值
from sklearn import metrics
print(metrics.classification_report(test_target, predict_target))
print(metrics.confusion_matrix(test_target, predict_target))
X = test_data
L1 = [n[0] for n in X]
print(L1)
L2 = [n[1] for n in X]
print(L2)
plt.scatter(L1, L2, c=predict_target, marker='x')
plt.title("DecisionTreClassifier")
plt.show()
########################################决策树分析###################
