import matplotlib.pyplot as plt
import random
import matplotlib
from matplotlib import font_manager

####################################################################################
# fig = plt.figure(figsize=(20, 8), dpi=80)
#
# x = range(2,26,2)
# y = [15,13,14.5,17,20,25,26,26,24,22,18,15]
#
# plt.plot(x,y)
# plt.xticks(x) #设置x的刻度
# plt.xticks(x[::2])#当刻度太密集的时候使用列表的步长(间隔取值)来解决？
# plt.savefig("./res/sigSize.png")
# plt.show()
##################################################################################
plt.figure(figsize=(20,8))
x = range(120)

random.seed(10) #设置随机种子，让不同的时候随机得到的结果都一样
y = [random.uniform(20, 35) for i in range(120)]

# print("y:",y)

plt.plot(x,y)

#设置支持中文显示
# myFont = font_manager.FontProperties(fname="/System/Library/Fonts/PingFang.ttc")

#设置x轴上字符串的刻度
_x_ticks = ['10点{}分'.format(i) for i in x if i < 60]
# print("_x_ticks: before ", _x_ticks)
_x_ticks += ["11点{}分".format(i-60) for i in x if i > 60]
# print("_x_ticks: after ", _x_ticks)

#让列表x中的数据和_x_ticks上的数据都传入，最终会再在x轴上一一对应的显示出来
#两组数据的长度必须一样，否制不能完全覆盖整个轴
#使用列表的切片，每隔5个选一个数据进行展示
#为了让字符串不会覆盖，使用rotation选项，让字符串旋转90度显示
plt.xticks(x[::5], _x_ticks[::5], rotation=90)

plt.xlabel("time")
plt.ylabel("temperature")
plt.title("The temperatur between 10 and 11")


plt.savefig("./res/t1.png")
plt.show()