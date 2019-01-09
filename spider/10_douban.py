# coding=utf-8
import requests
import json


class DoubanSpider:
    def __init__(self):
        self.urlTempList = [
            {   #动漫
                "urlTemp": "https://m.douban.com/rexxar/api/v2/subject_collection/tv_animation/items?start={}&count=18&loc_id=108288",
                "country": "DM"
            },
            {   #英美
                "urlTemp": "https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?start={}&count=18&loc_id=108288",
                "country": "YM"
            },
            {   #综艺
                "urlTemp": "https://m.douban.com/rexxar/api/v2/subject_collection/tv_variety_show/items?start={}&count=18&loc_id=108288",
                "country": "ZY"
            },
            {   #日剧
                "urlTemp": "https://m.douban.com/rexxar/api/v2/subject_collection/tv_japanese/items?start={}&count=18&loc_id=108288",
                "country": "RJ"
            }
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
            "Referer": "https://m.douban.com/movie/"
        }

    def parseUrl(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode('utf-8')

    def getContentList(self, jsonStr):
        dictRet = json.loads(jsonStr)
        contentList = dictRet['subject_collection_items']
        total = dictRet["total"]
        return contentList,total

    def saveContentList(self, contentList, country):
        with open("./res/"+country+"_douban.txt", "a", encoding='utf-8') as f:
            for content in contentList:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print(country+"保存成功")

    def run(self):  # 实现主要逻辑
        # 1.start_url
        # 2.发送请求
        # 3.提取数据
        # 4.保存
        # 5.构造下一页的url地址，进入循环
        for item in self.urlTempList:
            # item = self.urlTempList[2]
            num = 0
            total = 100 #假设有第一页
            while num < total+18:
                url = item['urlTemp'].format(num)
                jsonStr = self.parseUrl(url)
                contentList,total = self.getContentList(jsonStr)
                self.saveContentList(contentList, item['country'])
                # if len(contentList) < 18:
                #     break
                num += 18


if __name__ == '__main__':
    doubanSpider = DoubanSpider()
    doubanSpider.run()
