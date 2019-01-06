#coding=utf-8
import requests

session = requests.session()
postUrl = "http://www.renren.com/PLogin.do"
postData = {"email":"18390960948","password":"y20o8b93h10622"}
headersMy = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

#使用session发送post请求，cookie保存在其中
session.post(postUrl,data=postData, headers=headersMy)

#在使用session进行请求登陆之后才能访问的地址
r = session.get("http://home.renren.com/502645039/profile", headers=headersMy)

#保存页面
with open("renren.html", "w", encoding="utf-8") as f:
    f.write(r.content.decode())
