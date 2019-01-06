# coding=utf-8
import requests
import json
import sys

queryStr = sys.argv[1]

##转而使用手机页面，则发现少了许多参数
headersMy = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"}
fromUrl = "https://fanyi.baidu.com/langdetect"
dataFrom = {
    "query" : queryStr
}
rFrom = requests.post(fromUrl, data=dataFrom, headers=headersMy)
dictFromRes = json.loads(rFrom.content.decode())
fromLg = dictFromRes["lan"]
print(fromLg)

dataMy = {
    "from" : fromLg,
    "to" : "ch", #en
    "query" : queryStr
    # "transtype" : "translang",
    # "simple_means_flag" : "3",
    # "token" : "caa42a6acb21f0acf706908166429b31"
}
postUrl = "https://fanyi.baidu.com/basetrans"
r = requests.post(postUrl, data=dataMy, headers=headersMy)
# print(r.content.decode())
dictRes = json.loads(r.content.decode())
ret = dictRes["trans"][0]["dst"]
print("翻译结果为:", ret)

