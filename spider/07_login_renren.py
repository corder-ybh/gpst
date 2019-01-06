#coding=utf-8
import requests

session = requests.session()
postUrl = "http://www.renren.com/PLogin.do"
postData = {"email":"18390960948","password":"y20o8b93h10622"}
headersMy = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Cookie" : "anonymid=jqkia4if-ryc1xj; depovince=GW; _r01_=1; ick_login=41890075-35d6-4102-9e34-c0102e7b26d7; _ga=GA1.2.408248045.1546755535; _gid=GA1.2.646653833.1546755535; first_login_flag=1; ln_uact=18390960948; ln_hurl=http://hdn.xnimg.cn/photos/hdn121/20150331/2255/main_QxX6_75290003911b195a.jpg; wp=1; wp_fold=1; jebecookies=15f976de-5fa5-44f5-8800-8f173356e04b|||||; _de=24FBAFFFF80DC278D9E54D30AB3AAF2F; p=2547e019373eb990031788800d4bd5a19; t=2e9777a35ba091d086e594eb64d64a1a9; societyguester=2e9777a35ba091d086e594eb64d64a1a9; id=502645039; ver=7.0; JSESSIONID=abcuHbkyeywKXbVYo2HGw; xnsid=de269666; loginfrom=null"
        }

#在使用session进行请求登陆之后才能访问的地址
r = requests.get("http://home.renren.com/502645039/profile", headers=headersMy)

#保存页面
with open("renren2.html", "w", encoding="utf-8") as f:
    f.write(r.content.decode())
