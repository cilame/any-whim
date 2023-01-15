import re
import base64
import time
import json
import pprint
import requests
import random

interface = 'http://127.0.0.1:18089'
# interface = 'http://8.130.11.250:18089'

config_url = interface + '/config'
run_script_url = interface + '/run_script'

def run(proxy=None):
    def get_random_str(num):
        ls = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join([random.choice(ls) for i in range(num)])
    username = get_random_str(10)
    password = get_random_str(10)
    data = {
        "username":username,
        "password":password,
        "rememberMe":True,
        "market":"US",
        "transactionSubType":"signin",
        "reputation":{
            "ccAgentName":"WebApp",
            "platform":"Web",
            "market":"US",
            "deviceFingerprint":""
        }
    }
    data = {
        "match_url": "/bff/account/signin",
        "url": "https://www.starbucks.com/bff/account/signin",
        "method": "POST",
        "data": json.dumps(data, separators=(',', ':')),
    }
    s = requests.post(run_script_url, data=data).json()
    if s['status'] == 'success':
        s = s['message']
        url = s['url']
        data = s['postData']
        headers = s['headers']
        # pprint.pprint(headers)
        print('len(X-DQ7Hy5L1-a)', len(s['headers']['X-DQ7Hy5L1-a']))
        proxies = {'http':proxy, 'https':proxy} if proxy else None
        s = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=15)
        print(s)
        print(s.text)
    else:
        print(s['message'])


def init(proxy=None):
    headers = {
        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
        "accept-language": "zh-CN,zh;q=0.9",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.3440.75 Safari/537.36"
    }
    print('使用代理', proxy)
    proxies = {'http':proxy, 'https':proxy} if proxy else None
    u1 = 'https://www.starbucks.com/vendor/static/vendor2.js'
    print('本地请求1', u1)
    t1 = requests.get('https://www.starbucks.com/vendor/static/vendor2.js', headers=headers, proxies=proxies).text
    u2 = 'https://www.starbucks.com' + re.findall(r'"([^"]+/static/vendor2[^"]+)"', t1)[0]
    print('本地请求2', u2)
    t2 = requests.get(u2, headers=headers, proxies=proxies).text
    initer = [
        ['https://www.starbucks.com/account/signin?ReturnUrl=%2F', 'VM9xH+asjWTH2i7kzLA9AFX7MkbE7HjFmExRRogHOzJN8pZobaEPEKpeltwvASTQc+JRiMXzdw9dqP9vcLXDLocGBt8jAz9O9tb8kQ9NF0/o6bwP8BLcqiy5IogW/SupbefYi3jS0mLJVTIjVl9EfS/a/FH+YqsHsq7UKpCQPtsJBNVQwDpAHgGrNRosTWS1A4slGCN4UHW88pQ301L32FYGw4G8IfAttAx/ElBR4wkJPJfWIRCrevN4cU50zWjRu7kC8oYNshLWDdjbUyZy9g==', 'aes'],
        [u1, t1],
        [u2, t2],
    ]
    for i in initer:
        data = { 'match_url': i[0] }
        if len(i) > 1: data['value'] = i[1]
        if len(i) > 2: data['vtype'] = i[2]
        s = requests.post(config_url, data=data).json()
    data = { "url": "https://www.starbucks.com/account/signin?ReturnUrl=%2F", "userAgent": headers["user-agent"] }
    if proxy: data['proxy'] = proxy
    s = requests.post(config_url, data=data)

proxy = 'http://127.0.0.1:7890'
proxy = None

init(proxy=proxy)
print('初始化结束，等待页面加载，通常只执行一次。')
time.sleep(3) # 等待请求
for i in range(3):
    run(proxy=proxy)

