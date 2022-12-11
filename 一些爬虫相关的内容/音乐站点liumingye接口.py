# http://lab.liumingye.cn/api/?page=homePage

import time
import base64
import hashlib
import re, json
from urllib import request, parse
from urllib.parse import quote, unquote, urlencode

def md5(s): 
    return hashlib.md5(s.encode()).hexdigest()

def rc4(data, 
        key = b'default-key', 
        mode = "encode", 
        enfunc=base64.b64encode, 
        defunc=lambda q:bytes(ord(i) for i in base64.b64decode(q).decode()),
        ):
    if mode == "decode": data = defunc(data)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    R = []
    for c in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = c ^ (S[(S[i] + S[j]) % 256])
        R.append(t)
    if mode == "encode": return enfunc(bytes(R))
    return bytes(R)

def get_param_data(k):
    today = str(int(time.time() * 1000))
    tomorrow = str(int(time.time()) + 86400)
    ab = md5("G4N/_e[=!(+zFROT")[:30]
    ag = md5(ab[:16])
    ah = md5((ab + '9b')[16:32])[:16]
    H = md5(str(today))[32-4:] # 这里的时间是 “当前的时间” (毫秒)
    af = ag + md5(ag+H)
    K = tomorrow + md5(k + ah + '5' + 'b39ea286967cc0' + '3')[:16] + k # 这里的时间是 “当前时间加一天” (秒)
    v = H + rc4(K.encode(), (af*4).encode()).decode().strip('==')
    return v

def mk_url_headers_body(songid):
    url = (
        'http://tool.liumingye.cn/music/ajax/search'
    )
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    k = "text=https://y.qq.com/n/yqq/playlist/{}.html&page=1&type=YQA".format(songid)
    v = get_param_data(k)
    print('被加密参数:', k)
    print('加密后参数:', v)
    body = {
        "data": v
    }
    return url,headers,body

method = 'POST'
url, headers, body = mk_url_headers_body(7227193109)
JSONString = False #，这里通常为False，极少情况需要data为string情况下的json数据，如需要，这里设置为True
body = json.dumps(body).encode('utf-8') if JSONString else urlencode(body).encode('utf-8')
r = request.Request(url, method=method)
for k, v in headers.items():
    if k.lower() == 'accept-encoding': continue # urllib并不自动解压缩编码，所以忽略该headers字段
    r.add_header(k, v)
s = request.urlopen(r, data=body)
content = s.read().decode('utf-8')
jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
for i in jsondata['data']['list']:
    d = {}
    d["time"]     = i.get("time")
    d["artist"]   = i.get("artist")
    d["url_flac"] = i.get("url_flac")
    d["name"]     = i.get("name")
    d["lrc"]      = i.get("lrc")
    d["cover"]    = i.get("cover")
    d["url"]      = i.get("url")
    d["url_m4a"]  = i.get("url_m4a")
    d["url_128"]  = i.get("url_128")
    d["url_320"]  = i.get("url_320")
    print('------------------------------ split ------------------------------')
    import pprint
    pprint.pprint(d)
