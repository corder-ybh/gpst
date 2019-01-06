# -*- coding: UTF-8 -*-
import requests


class TiebaSpider:
    def __init__(self, tiebaName):
        self.tiebaName = tiebaName
        self.urlTemp = "https://tieba.baidu.com/f?kw=" + tiebaName + "&pn={}"
        self.headersMy = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    # 1、构造url列表
    def getUrlList(self):
        urlList = []  # 列表
        for i in range(1000):
            urlList.append(self.urlTemp.format(i * 50))
        return urlList

    # 发送请求，获取响应
    def parseUrl(self, url):
        print(url)
        response = requests.get(url, headers=self.headersMy)
        return response.content.decode()

    # 保存网页html字符串
    def saveHtml(self, htmlStr, pageNum):
        filePath = "./res/{}-第{}页.html".format(self.tiebaName, pageNum)
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(htmlStr)

    def run(self):  # 实现主要逻辑
        # 1、构造url列表
        urlList = self.getUrlList();
        # 2、遍历，发送请求，获取响应
        for url in urlList:
            htmlStr = self.parseUrl(url)
            # 3、保存
            pageNum = urlList.index(url) + 1  # index从0开始的
            self.saveHtml(htmlStr, pageNum)


if __name__ == '__main__':
    tiebaSpider = TiebaSpider("剑网3")
    tiebaSpider.run()
