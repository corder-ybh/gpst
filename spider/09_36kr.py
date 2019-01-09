# coding=utf-8
import json
import re
from parse_url import parse_url

url = "http://36kr.com/"
headers = {
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
}



htmlStr = parse_url(url, headers)

ret = re.findall("<script>var props=(.*?),locationnal=", htmlStr)[0]

with open("./res/36kr.json", "w", encoding='utf-8') as f:
    f.write(ret)

# ret = json.loads(ret)
# print(ret)
