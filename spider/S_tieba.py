# coding=utf-8
import requests
from lxml import etree
import json
import re
from urllib.parse import unquote
import time
import os


class TiebaSpider:
    def __init__(self, tiebaName):
        self.tiebaName = tiebaName
        self.host = "http://tieba.baidu.com/mo/q---,sz@320_240-1-3"
        self.startUrl = self.host + "/m?kw=" + tiebaName + "&pn=0"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def parseUrl(self, url):
        # 暂停防止被封
        # time.sleep(1)
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content  # .decode("utf-8")[38:]

    # 处理图片列表获取原图
    def opImg(self, imgList, title):
        if len(imgList) == 0:
            return None

        res = []
        for img in imgList:
            # print("img:" + img)
            urlTmp = re.search("&src=.*", img).group(0)[5:]
            url = unquote(urlTmp, 'utf-8')
            self.saveImg(url, title)
            res.append(url)
        return res

    #获取帖子内容
    def getContentList(self, htmlStr):
        # print(htmlStr)
        html = etree.HTML(htmlStr)
        divList = html.xpath("//div[contains(@class,'i')]")
        contentList = []
        for div in divList:
            item = {}
            item['title'] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()")[0]) > 0 else None
            item['href'] = self.host + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href")[0]) > 0 else None
            item['imgList'] = self.opImg(self.getImgList(item['href'], []), item['title'])
            contentList.append(item)
        # 提取下一页的url地址
        nextUrl = self.host + html.xpath("//a[text()='下一页']/@href")[0] if len(
            html.xpath("//a[text()='下一页']/@href")) > 0 else None
        return contentList, nextUrl

    # 获取帖子中的所有图片
    def getImgList(self, detailUrl, totalImgList):
        # print("detailUrl: " + detailUrl)
        detailHtmStr = self.parseUrl(detailUrl)
        # print(detailHtmStr)

        detailHtm = etree.HTML(detailHtmStr)
        imgList = detailHtm.xpath("//img[@class='BDE_Image']/@src")
        totalImgList.extend(imgList)

        detailNextUrl = detailHtm.xpath("//a[text()='下一页']/@href")
        if len(detailNextUrl) > 0:
            detailNextUrl = self.host + detailNextUrl[0]
            return self.getImgList(detailNextUrl, totalImgList)
        else:
            return totalImgList

    # 保存数据
    def saveContentList(self, contentList):
        filePath = './res/' + self.tiebaName + '.txt'
        with open(filePath, "a", encoding='utf-8') as f:
            for content in contentList:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")

    #保存图片
    def saveImg(self, imgUrl, title):
        imgContent = self.parseUrl(imgUrl)
        fileDict = "./res/" + self.trStr(title) + "/"
        isExists = os.path.exists(fileDict)

        if not isExists:
            os.mkdir(fileDict)

        filePth = fileDict + self.trStr(imgUrl[39:])
        with open(filePth, 'wb') as f:
            f.write(imgContent)

    def trStr(self, Str):
         return re.sub('[!@#$/?]', '', Str)

    # 主要逻辑
    def run(self):
        # 1.start_url
        # 2.发送请求，获取响应
        # 3.提取数据
        # 3.1提取列表页的url地址，获取详情页的第一页
        # 3.2请求列表页的url地址，获取详情页的第一页
        # 3.3提取详情页第一页的图片，提取下一页的地址
        # 3.4请求详情页下一页的地址，进入循环
        # 4.保存
        # 5.请求下一页的url
        nextUrl = self.startUrl
        i = 0  # nextUrl is not None:
        while i < 3:
            print(str(i) + "nextUrl: " + nextUrl)
            htmlStr = self.parseUrl(nextUrl)
            contentList, nextUrl = self.getContentList(htmlStr)
            self.saveContentList(contentList)
            i = i + 1


if __name__ == '__main__':
    tiebaSpider = TiebaSpider('李毅')
    tiebaSpider.run()
