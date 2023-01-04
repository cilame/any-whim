import re
import base64
import time
import json
import pprint
import requests
import random

interface = 'http://127.0.0.1:18089'
interface = 'http://8.130.11.250:18089'

proxy = 'http://127.0.0.1:7890'
proxy = None

def get_random_str(num):
    ls = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join([random.choice(ls) for i in range(num)])

import vthread
# @vthread.pool(10)
def run(show_req_info=True):
    url = interface + '/run_script'
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
    s = requests.post(url, data=data).json()
    if s['status'] == 'success':
        s = s['message']
        if s['method'] == 'GET':
            url = s['url']
            method = s['method']
            headers = s['headers']
            if show_req_info:
                print(url)
                print(method)
                pprint.pprint(headers)
            proxies = {'http':proxy, 'https':proxy} if proxy else None
            s = requests.get(url, headers=headers, proxies=proxies)
        elif s['method'] == 'POST':
            url = s['url']
            method = s['method']
            data = s['postData']
            headers = s['headers']
            if show_req_info:
                print(url)
                print(method)
                print(data)
                pprint.pprint(headers)
            proxies = {'http':proxy, 'https':proxy} if proxy else None
            s = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=15)
        print(s)
        print(s.text)
    else:
        print(s['message'])


def init():

    print('使用代理', proxy)
    proxies = {'http':proxy, 'https':proxy} if proxy else None
    u1 = 'https://www.starbucks.com/vendor/static/vendor2.js'
    print('本地请求1', u1)
    t1 = requests.get('https://www.starbucks.com/vendor/static/vendor2.js', proxies=proxies).text
    bt1 = base64.b64encode(t1.encode()).decode()
    u2 = 'https://www.starbucks.com' + re.findall(r'"([^"]+/static/vendor2[^"]+)"', t1)[0]
    print('本地请求2', u2)
    t2 = requests.get(u2, proxies=proxies).text
    bt2 = base64.b64encode(t2.encode()).decode()
    config_url = interface + '/config'
    initer = [
        ['https://www.starbucks.com/account/signin?ReturnUrl=%2F', 'PCFET0NUWVBFIGh0bWw+CjxodG1sPgo8aGVhZD4KICA8dGl0bGU+PC90aXRsZT4KPC9oZWFkPgo8Ym9keT4KCiAgPGgxPnZ2djwvaDE+CiAgPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iaHR0cHM6Ly93d3cuc3RhcmJ1Y2tzLmNvbS92ZW5kb3Ivc3RhdGljL3ZlbmRvcjIuanMiPjwvc2NyaXB0PgoKPC9ib2R5Pgo8L2h0bWw+', 'base64'],
        [u1, bt1, 'base64'],
        [u2, bt2, 'base64'],
    ]
    print('这里到最后的请求如果在多线程程序中需要加锁')
    costtime = time.time()
    for i in initer:
        data = { 'type': 'init_match', 'match_url': i[0] }
        if len(i) > 1: data['value'] = i[1]
        if len(i) > 2: data['vtype'] = i[2]
        s = requests.post(config_url, data=data).json()
    print('配置返回内容结束。')
    data = {
        "type": "init_page",
        "url": "https://www.starbucks.com/account/signin?ReturnUrl=%2F",
        "userAgent": "",
    }
    if proxy: data['proxy'] = proxy
    print('伪请求这个页面')
    s = requests.post(config_url, data=data)
    print(s)
    print('加锁配置耗时', time.time() - costtime)
    print('后面的配置只要不修改当前页面就可以用这个页面构造请求')

init()
print('初始化结束，等待页面加载，通常只执行一次。')
time.sleep(1)

for i in range(3):
    run(show_req_info=False)