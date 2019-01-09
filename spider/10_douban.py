# coding=utf-8
import requests
import json

class DoubanSpider:
    def __init__(self):
        self.url_temp_list = [
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count=18&loc_id=108288",
                "country": "US"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start={}&count=18&loc_id=108288",
                "country": "UK"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start={}&count=18&loc_id=108288",
                "country": "CN"
            }
        ]
        self.headers = []