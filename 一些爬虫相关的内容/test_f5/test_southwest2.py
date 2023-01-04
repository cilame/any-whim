import time
import json
import pprint
import base64
import requests
import random

interface = 'http://127.0.0.1:18089'
interface = 'http://8.130.11.250:18089'

proxy = 'http://127.0.0.1:7890'
proxy = None

# import vthread
# @vthread.pool(10)
def run(show_req_info=True):
    url = interface + '/run_script'
    data = {
        "match_url": "/api/security/v3/security/authorize",
        "url": "https://www.southwest.com/api/security/v3/security/authorize",
        "method": "POST",
        "headers": json.dumps({
            'content-type': 'application/x-www-form-urlencoded',
            'x-api-key': 'l7xx944d175ea25f4b9c903a583ea82a1c4c',
            'x-channel-id': 'southwest',
            'x-user-experience-id': 'd51a29db-c5b7-4b3c-9413-b587330b04ee',
        }),
        "data": "username=123%40123.com&password=asdfasdf&application=landing-home-page&site=southwest&client_id=5f12a3bf-9e48-46a9-8751-84cc5fad6643&scope=openid&response_type=id_token+swa_token",
    }
    s = requests.post(url, data=data).json()
    if s['status'] == 'success':
        s = s['message']
        if s['method'] == 'GET':
            url = s['url']
            method = s['method']
            headers = s['headers']
            print(url)
            if show_req_info:
                print(method)
                pprint.pprint(headers)
            s = requests.get(url, headers=headers)
        elif s['method'] == 'POST':
            url = s['url']
            method = s['method']
            data = s['postData']
            headers = s['headers']
            print(url)
            if show_req_info:
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

    u1 = 'https://www.southwest.com/assets/app/scripts/swa-common.js'
    print('本地请求', u1)
    t1 = requests.get(u1, proxies=proxies).text
    bt1 = base64.b64encode(t1.encode()).decode()

    config_url = interface + '/config'
    initer = [
        ['https://www.southwest.com/', "PCFET0NUWVBFIGh0bWw+CjxodG1sPgo8aGVhZD4KICA8dGl0bGU+PC90aXRsZT4KPC9oZWFkPgo8Ym9keT4KCiAgPGgxPnZ2djwvaDE+CiAgPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iaHR0cHM6Ly93d3cuc291dGh3ZXN0LmNvbS9hc3NldHMvYXBwL3NjcmlwdHMvc3dhLWNvbW1vbi5qcyI+PC9zY3JpcHQ+Cgo8L2JvZHk+CjwvaHRtbD4=", 'base64'],
        [u1, bt1, 'base64']
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
        "url": "https://www.southwest.com/",
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