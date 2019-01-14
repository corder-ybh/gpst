# coding=utf-8
import requests
from lxml import etree
import json
from queue import Queue
import threading

class QiuBai:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.urlQueue = Queue()
        self.htmlQueue = Queue()
        self.contentQueue = Queue()

    '''
    获取所有页面的url，并返回urllist
    '''
    def getTotalUrl(self):
        urlTemp = "https://www.qiushibaike.com/hot/page/{}/"
        for i in range(1, 36):
            self.urlQueue.put(urlTemp.format(i))
        print("getTotalUrl is over")

    '''
    发送请求，获取响应，同事etree处理html
    '''
    def parseUrl(self):
        while self.urlQueue.not_empty:
            url = self.urlQueue.get()
            print("parsing Url: ", url)
            response = requests.get(url, headers=self.headers, timeout=10)
            #获取html字符串
            html = response.content.decode()
            # print(html)
            # exit()
            #获取element类型的html
            html = etree.HTML(html)
            self.htmlQueue.put(html)
            #放在此处，保证url已经获得反馈以后再将url设置为任务已完成
            self.urlQueue.task_done()
        print("parseUrl is over")

    '''
    返回一个list，包含一个url对应页面的所有段子的所有内容的列表
    '''
    def getContent(self):
        print("getContent start!")
        while self.htmlQueue.not_empty:
            html = self.htmlQueue.get()
            totalDiv = html.xpath("//*[starts-with(@id, 'qiushi_tag_')]")
            items = []
            #遍历totalDiv，获取段子的所有信息
            for i in totalDiv:
                author_img = i.xpath('./div[@class="author clearfix"]/a[1]/img/@src')
                author_img = "https:" + author_img[0] if len(author_img) > 0 else None
                author_name = i.xpath('./div[@class="author clearfix"]/a[2]/h2/text()')
                author_name = author_name[0] if len(author_name) > 0 else None
                author_href = i.xpath('./div[@class="author clearfix"]/a[1]/@href')
                author_href = "https://www.qiushibaike.com" + author_href[0] if len(author_href) > 0 else None
                author_gender = i.xpath('./div[@class="author clearfix"]//div/@class')
                author_gender = author_gender[0].split(" ")[-1].replace("Icon", "") if len(author_gender) > 0 else None
                author_age = i.xpath('./div[@class="author clearfix"]//div/text()')
                author_age = author_age[0] if len(author_age) > 0 else None
                content = i.xpath('./a[@class="contentHerf"]/div/span/text()')
                content_vote = i.xpath('./div[@class="stats"]/span[1]/i/text()')
                content_vote = content_vote[0] if len(content_vote) > 0 else None
                content_comment_numbers = i.xpath('./div[@class="stats"]/span[2]/a/i/text()')
                content_comment_numbers = content_comment_numbers[0] if len(content_comment_numbers) > 0 else None
                hot_comment_author = i.xpath('./a[@class="indexGodCmt"]/div/span[last()]/text()')
                hot_comment_author = hot_comment_author[0] if len(hot_comment_author) > 0 else None
                hot_comment = i.xpath('./a[@class="indexGodCmt"]/div/div/text()')
                hot_comment = hot_comment[0].replace("\n：", "").replace("\n", "") if len(hot_comment) > 0 else None
                hot_comment_like_num = i.xpath('./a[@class="indexGodCmt"]/div/div/div/text()')
                hot_comment_like_num = hot_comment_like_num[-1].replace("\n", "") if len(
                hot_comment_like_num) > 0 else None
            item = dict(
                author_name=author_name,
                author_img=author_img,
                author_href=author_href,
                author_gender=author_gender,
                author_age=author_age,
                content=content,
                content_vote=content_vote,
                content_comment_numbers=content_comment_numbers,
                hot_comment=hot_comment,
                hot_comment_author=hot_comment_author,
                hot_comment_like_num=hot_comment_like_num
            )
            items.append(item)
            self.contentQueue.put(item)
            self.htmlQueue.task_done()

    '''
    保持items
    '''
    def saveItems(self):
        print("saveItems start")
        while self.contentQueue.not_empty:
            items = self.contentQueue.get()
            f = open('./res/qb.txt', "a")
            for i in items:
                json.dump(i, f, ensure_ascii=False, indent=2)
            f.close()
            self.contentQueue.task_done()

    '''
    获取url list
    url_list = self.getTotalUrl
    '''
    def run(self):
        threadList = []

        threadUrl = threading.Thread(target=self.getTotalUrl())
        threadList.append(threadUrl)
        #发送网络请求
        for i in range(10):
            threadParse = threading.Thread(target=self.parseUrl())
            threadList.append(threadParse)

        #提取数据
        threadGetContent = threading.Thread(target=self.getContent())
        threadList.append(threadGetContent)
        #保存
        threadSave = threading.Thread(target=self.saveItems())
        threadList.append(threadSave)
        for t in threadList:
            t.setDaemon(True)  #为每个进程设置为后台进程，效果是如果主进程退出子进程也会退出
            t.start()

        #让主线程等待，所有的队列为空的时候才能退出
        self.urlQueue.join()
        self.htmlQueue.join()
        self.contentQueue.join()

if __name__ == '__main__' :
    qiubai = QiuBai()
    qiubai.run()


