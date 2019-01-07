# coding=utf-8
import json
import requests
from parse_url import parse_url
url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?start=0&count=18&loc_id=108288"
htmStr = parse_url(url)
print(htmStr)
# ret = json.load(htmStr)
# print(ret)

