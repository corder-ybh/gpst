# -*- coding: UTF-8 -*-
import requests

headerMe = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
p={"wd":"长城"}
urlTmp="http://www.baidu.com/s"
#此处headers不能直接将值写进去
response  = requests.get(url=urlTmp, headers=headerMe, params=p)
print(response.status_code)
assert response.status_code == 200
# print(response.headers)
# print(response.request.headers)
print(response.content.decode("utf-8"))
print(response.url)