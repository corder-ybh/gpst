import requests
from retrying import retry

headers = {
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"
}

def _pare_url(url, method, data, proxies):
    print("*" * 20)
    if method == "POST":
        response = requests.post(url, data=data, headers=headers, proxies=proxies)
    else:
        response = requests.get(url, headers=headers, timeout=3, proxies=proxies)
    assert response.status_code == 200
    return response.content.decode()

def parse_url(url, method="Get", data=None, proxies={}):
    try:
        htmStr = _pare_url(url, method, data, proxies)
    except:
        htmStr = None
    return htmStr

if __name__ == '__main__':
    url = "http://www.baidu.com"
    print(parse_url(url))