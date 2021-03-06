# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import ItcastItem

class ItcastSpider(scrapy.Spider):
    #以下3个属性都是必须的
    name = 'itcast'  #爬虫的识别名称，必须是唯一的
    allowed_domains = ['itcast.cn']  #搜索的域名范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml'] #爬取的url元祖/列表，怕从从这里开始抓取数据

    #解析的方法
    def parse(self, response):
        # with open("teacher.html", "w", encoding='utf-8') as f:
        #     f.write(response.text)
        items = []

        for each in response.xpath("//div[@class='li_txt']"):
            #将我们得到的数据封装到一个 'ItcastItem'对象
            item = ItcastItem()
            #extract(0方法返回的都是字符串
            name = each.xpath("h3/text()").extract()
            title = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()

            #xpath返回的是包含一个元素的列表
            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]

            # items.append(item)
            # 将获取的数据交给pipelines
            yield item

        #直接返回最后数据
        # return items
