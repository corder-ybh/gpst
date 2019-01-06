# -*- coding: UTF-8 -*-
#特征抽取
# from sklearn.feature_extraction.text import CountVectorizer
#
# vector = CountVectorizer()
#
# res = vector.fit_transform(["life is short, i like xx", "left is to long, i dislike python"])
#
# print(vector.get_feature_names())
# print(res.toarray())

#字典数据抽取
from sklearn.feature_extraction import DictVectorizer
#文本特征抽取
from sklearn.feature_extraction.text import CountVectorizer
#中文分词
import jieba

def dictvec():
    '''
    字典数据抽取：把字典中的一些类别数据，分别进行转换成特征
    对于数组形式，有类别的这些特征，先要转换成字典数据
    :return:None
    '''
    #实例化
    dict = DictVectorizer(sparse=False)
    #调用fit_transform
    data = dict.fit_transform([{'city':'北京','temperature':100}, {'city':'深圳','temperature':80}, {'city':'上海','temperature':90}])

    print(dict.get_feature_names())
    #转换成one-hot编码：为每个类别生成一个布尔列，有该属性则为1，无则为0
    print(data)

    #基本用不到
    print(dict.inverse_transform(data))

    return None

'''
文本特征抽取：对文本数据进行特征抽取
对文本进行特征值化
'''
def countvec():
    cv = CountVectorizer()
    data = cv.fit_transform(["life is short, i like xx", "left is to long, i dislike python"])

    print(cv.get_feature_names()) #词的列表，单个字母不统计(单个字母对文章主题往往无意义)，
    # 也不支持中文词语区分(中文需要结合分词，jieba)
    # print(data)
    print(data.toarray()) #对词的出现次数进行统计
    #用途很多
    #1、文本分类
    #2、情感分析
    #
    return None

def cutWord(str):
    con1 = jieba.cut(str)
    # print(con1)
    content1 = list(con1)
    c1 = ' '.join(content1)
    # print(c1)
    return c1

'''
中文特征值化
'''
def hanzivec():
    cv = CountVectorizer()
    data = cv.fit_transform([cutWord("网易娱乐11月25日报道 近日，高晓松在《奇葩说》中表示自己很像吴亦凡，引发网友讨论。随后，高晓松发微博表示：“在《奇葩说》里说的话都是为了辩论的立场，并不代表本人观点，包括但不限于本人年轻时长得帅，万人迷等，不成熟的小记忆啊！”。高晓松自称像吴亦凡后，有网友吐槽这是吴亦凡被黑得最惨的一次，不过也有网友调侃吴亦凡“长大后你就成了他”。"), cutWord("寒窗苦读，无非是想考个好学校，有个好未来。可是长葛市的黄女士却说：“我的寒窗十年就是一个笑话。到头来却发现学籍被人顶替了，而顶替学籍的人还是大伯家的女儿。”经过都市频道《都市报道》连续报道之后，有人给黄女士打来了一通神秘的和解电话......“要多少钱那边能出能接受，事就妥了...要他的钱给他说个数。如果要是不要钱了让他去你爸那坐坐，把事情说说，弟兄也和解了啥事也没有了，也别要道歉书、保证书了......”黄海霞说：如今她已经40多岁，用多少钱都买不回她的青春......")])

    print(cv.get_feature_names())  # 词的列表，单个字母不统计(单个字母对文章主题往往无意义)，
    # 也不支持中文词语区分(中文需要结合分词，jieba)
    # print(data)
    print(data.toarray())  # 对词的出现次数进行统计

    return None

"""
tfidf 比上一种好，解决了如两篇文章都有一样多的“所以” “因为” “我们”等中性词而被判断为同一类型文章的误判
TF：term frequence 词的频率
idf：逆文档频率inverse document frequency  log(总文档数量/该词出现文档数量) logX x越小log值越小
TF-IDF的主要思想是：如果某个词或短语在一篇文章中出现的概率高，并且在其他文章中很少出现，则认为此词或者短语
具有很好的类别区分能力，适合用来分类
TF-IDF作用：用以评估一字词对于一个文件集或者一个语料库中的其中一份文件的重要成都
"""

if __name__ == "__main__":
    # dictvec()
    # countvec()
    hanzivec()