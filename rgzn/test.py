# -*- coding: UTF-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import jieba

def countVec():
    '''
    对文本进行特征值化
    :return:
    '''
    c1 = hanziCut("现场演示新品技术这种事情相信各位都不会陌生，大到电脑、笔记本，小到手机、蓝牙音箱几乎各个厂商都曾在现场为我们演示过新产品特性。不过呢，现场失误这种事情毕竟是不可控的，比如今天中午雷军在北京召开的小米AIoT开发者大会，“小爱同学”便频频出错。")
    c2 = hanziCut("在今天的小米AIoT开发者大会上，雷军表示小米集团自2014年开始就已经开始了loT的布局，并且目前拥有智能连接数超过了1.32亿台，小爱同学累计激活设备数约1亿台，累计唤醒次数超过80亿，月活跃用户数超过3400万。")
    c3 = hanziCut("现场雷军更是出了几个问题来考小爱同学：“三个木念什么？”小爱同学：“你是电，你是光，你是唯一的...”。惹得最后雷军只能无奈的说到：小爱同学你是不是每次演示的时候都要出错啊。")

    '''
    文本分类，明天，我们这些中性词语应该权重放小
    tf-idf 朴素贝叶斯
    tf:term frequeacy 词的频率                  统计出现的次数
    idf:逆文档频率inverse document frequency    log(总文档数/该词出现的文档数)
    重要性 tf-idf = tf * idf  可以取出文档中哪些词是重要的，用以评估一字词对于一个文件集或一个语料库
    的其中一份文件的重要性
    主要思想：如果某个词或短语在一篇文章中出现的频率高，并且在其他文中中很少出现，
    则认为此词或短语具有很好的区分能力，适合用来分类
    TfidfVectorizer语法
    TfidfVectorizer(stop_words=None,...)
    TfidfVectorizer.fit_transform(X)
    X:文本或包含文本字符串的可迭代对象
    返回值：返回sparse矩阵
    TfidfVectorizer.inverse_transform(X)
    X:array数组或者sparse矩阵
    返回值:转换之前数据格式
    TfidfVectorizer.get_feature_names()
    返回值:单词列表
    '''
    cv = CountVectorizer()
    data = cv.fit_transform([c1, c2, c3])
    print(cv.get_feature_names())
    print(data.toarray())

    return None

def tfidfVec():
    '''
    对文本进行特征值化
    :return:
    '''
    c1 = hanziCut("现场演示新品技术这种事情相信各位都不会陌生，大到电脑、笔记本，小到手机、蓝牙音箱几乎各个厂商都曾在现场为我们演示过新产品特性。不过呢，现场失误这种事情毕竟是不可控的，比如今天中午雷军在北京召开的小米AIoT开发者大会，“小爱同学”便频频出错。")
    c2 = hanziCut("在今天的小米AIoT开发者大会上，雷军表示小米集团自2014年开始就已经开始了loT的布局，并且目前拥有智能连接数超过了1.32亿台，小爱同学累计激活设备数约1亿台，累计唤醒次数超过80亿，月活跃用户数超过3400万。")
    c3 = hanziCut("现场雷军更是出了几个问题来考小爱同学：“三个木念什么？”小爱同学：“你是电，你是光，你是唯一的...”。惹得最后雷军只能无奈的说到：小爱同学你是不是每次演示的时候都要出错啊。")

    '''
    文本分类，明天，我们这些中性词语应该权重放小
    tf-idf 朴素贝叶斯
    tf:term frequeacy 词的频率                  统计出现的次数
    idf:逆文档频率inverse document frequency    log(总文档数/该词出现的文档数)
    重要性 tf-idf = tf * idf  可以取出文档中哪些词是重要的，用以评估一字词对于一个文件集或一个语料库
    的其中一份文件的重要性
    主要思想：如果某个词或短语在一篇文章中出现的频率高，并且在其他文中中很少出现，
    则认为此词或短语具有很好的区分能力，适合用来分类
    TfidfVectorizer语法
    TfidfVectorizer(stop_words=None,...)
    TfidfVectorizer.fit_transform(X)
    X:文本或包含文本字符串的可迭代对象
    返回值：返回sparse矩阵
    TfidfVectorizer.inverse_transform(X)
    X:array数组或者sparse矩阵
    返回值:转换之前数据格式
    TfidfVectorizer.get_feature_names()
    返回值:单词列表
    分类机器学习算法的重要依据
    '''
    tf = TfidfVectorizer()
    data = tf.fit_transform([c1, c2, c3])
    print(tf.get_feature_names())
    print(data.toarray())

    return None

'''
特征预处理： 对数据进行处理-> 缺失值
1、特征预处理的方法，2、sklearn特征预处理API
特征预处理是：通过特地的统计方法(数学方法)将 数据转换成算法要求的数据

数值型数据：标准缩放
  1、归一化
  2、标准化
  
  3、缺失值
类别型数据：one-hot编码
时间类型：时间的切分  

sklearn特征处理API：sklearn.preprocessing

归一化处理：
通过对原始数据进行变换，把数据映射到(默认为[0,1])之间
公式： X' = (X-min) / (max - min)
 X" = X' * (mx -mi) + mi
 作用于每一列，max为一列的最大值，min为最小值，X"为最终结果,mx mi分别为指定区间值，默认mx=1 mi=0
 sklearn归一化API: sklearn.preprocessing.MinMaxScaler
 MinMaxScalar(feature_range=(0,1)...)
 MinMaxScalar.fit_transform(x)
 X:numpy array格式的数据[n_samples, n_features]
 返回值:转换后的形状相同的array
 归一化步骤
 1、实力和MinMaxScalar
 2、通过fit_transform转换
'''



'''
汉字分词
'''
def hanziCut(str):

    #切割为词语
    con = jieba.cut(str)
    #转换为列表
    content = list(con)
    #把列表转换成字符串
    cStr = ' '.join(content)
    # print(cStr)
    return cStr

if __name__ == "__main__":
    tfidfVec()