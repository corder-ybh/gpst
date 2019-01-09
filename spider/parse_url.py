import requests
#from retrying import retry

def _pare_url(url, method, data, proxies, headers):
    print("*" * 20)
    if method == "POST":
        response = requests.post(url, data=data, headers=headers, proxies=proxies)
    else:
        response = requests.get(url, headers=headers, timeout=3, proxies=proxies)
    # assert response.status_code == 200
    return response.content.decode('utf-8')

def parse_url(url, headers, method="Get", data=None, proxies={}, ):
    # try:
    htmStr = _pare_url(url, method, data, proxies, headers)
    # except:
    #     htmStr = None
    return htmStr

if __name__ == '__main__':
    url = "http://www.baidu.com"
    print(parse_url(url))