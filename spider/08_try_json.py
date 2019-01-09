# coding=utf-8
import json
import requests
from parse_url import parse_url
url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?start=0&count=18&loc_id=108288"
headers = {
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
"Referer": "https://m.douban.com/movie/"
}
htmStr = parse_url(url, headers)
# print(htmStr)
#注意lodas和load的区别
ret = json.loads(htmStr)
# print(ret)
with open("./res/douban.json", "w") as f:#, encoding="utf-8"
    f.write(json.dumps(ret, ensure_ascii=False, indent=4))

#json.load的使用
# with open("./res/douban.json", "r") as f:
#     ret2 = json.load(f)
#     print(ret2)
#     print(type(ret2))

#json.dump的使用
# with open("./res/douban1.json", "w") as f:
#     json.dump(ret, f, ensure_ascii=False, indent=4)