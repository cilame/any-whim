# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import unquote, quote, urlencode

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'


    def start_requests(self):
        def mk_detect_request(key, _to):
            def mk_url_headers_body(key):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://fanyi.baidu.com/langdetect'
                )
                url = quote_val(url)
                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://fanyi.baidu.com",
                    "pragma": "no-cache",
                    "referer": "https://fanyi.baidu.com/translate",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest"
                }
                body = {
                    "query": key
                }
                return url,headers,body
            url,headers,body = mk_url_headers_body(key)
            meta = {}
            meta['proxy'] = self.proxy
            meta['key'] = key
            meta['to'] = _to
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = urlencode(body),
                    callback = self.parse_detect_src,
                    meta     = meta,
                )
            return r
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.baidu.com/translate'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        # 
        keys = ['20世纪60年代，日本已经进入高度发达的资本主义社会。经济在快速发展，人们的精神危机也与日俱增。物质生活的丰富与人的欲求膨胀，造成了精神世界的严重失衡。人与人之间的交流减少，心理距离拉大。生活在都市的人们像无根的浮萍，孤独、虚无、失落，却又无力面对强大的社会压力。都市的繁华，掩饰不了人们内心的焦虑。']
        _from = None #'zh' # 这里如果设置为 None，则会自动增加一个请求过程：请求另一个接口先检测传入的 key 是哪国语言，然后再继续后续的翻译操作
        _to = 'en'

        for key in keys:
            if _from:
                url,headers = mk_url_headers()
                meta = {}
                meta['proxy'] = self.proxy
                meta['key'] = key
                meta['to'] = _to
                meta['from'] = _from
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_set_cookie_first,
                        meta     = meta,
                        dont_filter = True,
                    )
                yield r
            else:
                yield mk_detect_request(key, _to)

    def parse_detect_src(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.baidu.com/translate'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        meta['proxy'] = self.proxy
        meta['key'] = response.meta.get('key')
        meta['to'] = response.meta.get('to')
        meta['from'] = jsondata['lan']
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_set_cookie_first,
                meta     = meta,
                dont_filter = True,
            )
        yield r

    def parse_set_cookie_first(self, response):
        COOKIE  = response.headers.to_unicode_dict().get('set-cookie').split('; ', 1)[0]
        content = response.body.decode()
        gtk     = re.findall(r"window\.gtk *= *'(\d+.\d+)'", content)[0]
        token   = re.findall(r"token: *'([^']+)'", content)[0]
        key     = response.meta.get('key')
        def mk_url_headers(COOKIE):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.baidu.com/translate'
            )
            url = quote_val(url)
            headers = {
                "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "cookie": (
                    COOKIE
                ),
                "pragma": "no-cache",
                "referer": "https://fanyi.baidu.com/translate",
                "sec-fetch-dest": "image",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(COOKIE)
        meta = {}
        meta['proxy'] = self.proxy
        meta['key'] = response.meta.get('key')
        meta['COOKIE'] = COOKIE
        meta['to'] = response.meta.get('to')
        meta['from'] = response.meta.get('from')
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_sign_and_token,
                meta     = meta,
                dont_filter = True,
            )
        yield r

    def parse_sign_and_token(self, response):
        def get_sign(gtk, r):
            if len(r) > 30:
                _q = int(len(r)/2)-5
                r = r[:10] + r[_q:_q+10] + r[-10:]
            S = list(r.encode())
            a,b = gtk.split('.')
            m,s = int(a),int(b)
            p = m
            F = '+-a^+6'
            D = '+-3^+b+-f'
            def n(r, o):
                t = 0
                while (t < len(o) - 2):
                    a = o[t + 2]
                    a = ord(a[0]) - 87 if a >= "a" else int(a)
                    a = r >> a if "+" == o[t + 1] else r << a
                    r = r + a & 4294967295 if "+" == o[t] else r ^ a
                    t += 3
                return r
            for b in range(len(S)):
                p += S[b]
                p = n(p, F)
            p = n(p, D)
            p ^= s
            if 0 > p: p = (2147483647 & p) + 2147483648
            p %= 1e6
            return str(int(p))+'.'+str(int(p)^m)
        COOKIE  = response.meta.get('COOKIE')
        content = response.body.decode()
        gtk     = re.findall(r"window\.gtk *= *'(\d+.\d+)'", content)[0]
        token   = re.findall(r"token: *'([^']+)'", content)[0]
        key     = response.meta.get('key')
        sign    = get_sign(gtk, key)
        _to     = response.meta.get('to')
        _from   = response.meta.get('from')
        def mk_url_headers_body(COOKIE, key, sign, token, _to, _from):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.baidu.com/v2transapi'
                '?from={}'
                '&to={}'
            ).format(_from, _to)
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cookie": (
                    COOKIE
                ),
                "origin": "https://fanyi.baidu.com",
                "pragma": "no-cache",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            body = {
                "from": _from,
                "to": _to,
                "query": key,
                "transtype": "realtime",
                "simple_means_flag": "3",
                "sign": sign,
                "token": token,
                "domain": "common"
            }
            return url,headers,body
        url,headers,body = mk_url_headers_body(COOKIE, key, sign, token, _to, _from)
        meta = {}
        meta['proxy'] = self.proxy
        meta['key'] = key
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = urlencode(body),
                callback = self.parse_info,
                meta     = meta,
            )
        yield r

    def parse_info(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        # import pprint
        # pprint.pprint(jsondata, depth= None )
        d = {}
        d['key']        = response.meta.get('key')
        d['translate']  = jsondata['trans_result']['data'][0]['dst']
        d['from']       = jsondata['trans_result']['from']
        d['to']         = jsondata['trans_result']['to']
        d['infos']      = jsondata['trans_result']['data']
        d['keywords']   = jsondata['trans_result'].get('keywords')
        import pprint
        pprint.pprint(d, depth= None )
        yield d




# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/UlPnutCJQG'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        # 'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, csv, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
