# coding=utf-8
import requests
import time
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import random


def zhihuLogin(username, password):
    # 构建一个保存cookie值得session对象
    sessiona = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    # 先获取页面信息，找到需要post得数据（并记录当前页面的Cookie）
    html = sessiona.get('https://www.zhihu.com/#signin', headers=headers).content

    # print(html)

    # 找到name属性为_xsrf的input标签，去除value里的值
    # _xsrf = BeautifulSoup(html, 'lxml').find('input', attrs={'name':'_xsrf'}).get('value')

    # 取出验证码，r后面的值是unix时间戳，time.time()
    for i in range(0, 100):
        captchaUrl = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % ((time.time()) * 1000)
        print('-' * 100, captchaUrl)
        response = sessiona.get(captchaUrl, headers=headers)
        captcha(response.content)
    # print('*'*100, response)


def captcha(data):
    fileName = "captcha" + str(random.randint(1, 1000)) + '.jpg'
    with open('./cap/' + fileName, 'wb') as fp:
        fp.write(data)
    time.sleep(1)
    image = Image.open("./cap/" + fileName)
    text = pytesseract.image_to_string(image)
    print("识别后的验证码为", text)


if __name__ == "__main__":
    zhihuLogin('', '')
