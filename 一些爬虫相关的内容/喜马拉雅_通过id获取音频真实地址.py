# 通过喜马拉雅音频ID获取真实的媒体文件地址
# 直接执行脚本即可测试，无需额外第三方依赖
# 开发于 python3

import re, json
from urllib import request
from urllib.parse import urlencode

def mk_url_headers(url):
    headers = {
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    return url,headers

def myget(url, headers):
    r = request.Request(url, method='GET')
    for k, v in headers.items():
        if k.lower() == 'accept-encoding': continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r)

def get_media_url(jsondata):
    def decode_ximalaya(t):
        def some1(t, e):
            t = 'd{}9'.format(bt)
            n = [None]*len(t)
            r = 0
            while (r < len(t)):
                o = (ord(t[r]) - 97) if (ord("a") <= ord(t[r]) and ord("z") >= ord(t[r])) else (ord(t[r]) - ord("0") + 26)
                i = 0
                while (36 > i):
                    if (e[i] == o):
                        o = i
                        break
                    i; i += 1
                n[r] = chr((o - 26 + ord("0"))) if 25 < o else chr((o + 97))
                r += 1
            return ''.join(n)
        def some2(t):
            a = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1]
            o = len(t)
            r = 0
            i = []
            while r<o:
                e = a[255 & ord(t[r])]; r += 1
                while r<o and e == -1:
                    e = a[255 & ord(t[r])]; r += 1
                if e == -1: break
                n = a[255 & ord(t[r])]; r += 1
                while r<o and n == -1:
                    n = a[255 & ord(t[r])]; r += 1
                if n == -1: break
                v = e << 2 | (48 & n) >> 4
                i.append(v)
                e = 255 & ord(t[r]); r += 1
                if e == 61:
                    return i
                e = a[e]
                while r<o and e == -1:
                    e = 255 & ord(t[r]); r += 1
                    if e == 61:
                        return i
                    e = a[e]
                if e == -1: break
                v = (15 & n) << 4 | (60 & e) >> 2
                i.append(v)
                n = 255 & ord(t[r]); r += 1
                if n == 61:
                    return i
                n = a[n]
                while r<o and n == -1:
                    n = 255 & ord(t[r]); r += 1
                    if n == 61:
                        return i
                    n = a[n]
                if n == -1: break
                v = (3 & e) << 6 | n
                i.append(v)
            return i
        def some3(t, e):
            r = [None] * 256
            i = ""
            a = 0
            while 256 > a:
                r[a] = a
                a += 1
            o = 0
            a = 0
            while 256 > a:
                o = (o + r[a] + ord(t[a%len(t)])) % 256
                r[a], r[o] = r[o], r[a]
                a += 1
            u = 0
            o = 0
            a = 0
            while u < len(e):
                a = (a + 1) % 256
                o = (o + r[a]) % 256
                n = r[a]
                r[a] = r[o]
                r[o] = n
                i += chr(e[u] ^ r[(r[a] + r[o]) % 256])
                u += 1
            return i
        bt = "g3utf1k6yxdwi0"
        wt = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
        a = some1(bt, wt)
        b = some2(t)
        c = some3(a, b)
        n = c.split('-')
        d = {}
        d['sign']      = n[1]
        d['buy_key']   = n[0]
        d['token']     = n[2]
        d['timestamp'] = n[3]
        return d
    class GT:
        def __init__(self, t):
            self._randomSeed = t
            self._cgStr = ""
            self.cg_hun()
        def cg_hun(self):
            t = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890"
            e = len(t)
            for n in range(e):
                r = self.ran() * len(t)
                o = int(r)
                self._cgStr += t[o]
                t = ''.join(t.split(t[o]))
        def ran(self):
            self._randomSeed = (211 * self._randomSeed + 30031) % 65536
            return self._randomSeed/65535
        def cg_fun(self, t):
            t = t.split("*")
            e = ""
            for n in range(len(t)-1):
                e += self._cgStr[int(t[n])]
            return e
    seed = jsondata.get('seed')
    fileId = jsondata.get('fileId')
    domain = jsondata.get('domain')
    apiVersion = jsondata.get('apiVersion')
    params = decode_ximalaya(jsondata['ep'])
    params['duration'] = jsondata.get('duration')
    return domain.replace('http://', 'https://') + '/download/' + apiVersion + '/' + GT(seed).cg_fun(fileId) + '?' + urlencode(params)

if __name__ == '__main__':

    # 音频id，通常是下面这样地址的最后一部分数字为音频id（喜马拉雅的部分音频地址需要解密，有些没有加密的可以直接拿到音频地址则无需解密）
    # https://www.ximalaya.com/youshengshu/24593608/193884895
    mediaid = '193884895'

    url = 'https://mpay.ximalaya.com/mobile/track/pay/{}?device=pc&isBackend=true'.format(mediaid)
    url, headers = mk_url_headers(url)
    url = get_media_url(json.loads(myget(url, headers).read().decode()))
    print(url)