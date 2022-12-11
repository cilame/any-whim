# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import unquote, quote

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = 'http://127.0.0.1:7078'

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://translate.google.com/'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        keys = ['疯狂世界']
        _from = 'zh-CN'
        _to = 'en' # 日本为 ja

        for key in keys:
            url,headers = mk_url_headers()
            meta = {}
            meta['proxy'] = self.proxy
            meta['from'] = _from
            meta['to'] = _to
            meta['key'] = key
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_ttk,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r

    def parse_ttk(self, response):
        def get_sign(gtk, r):
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
        def mk_url_headers(sign, key, _from, _to):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://translate.google.com/translate_a/single'
                '?client=webapp'
                '&sl={}'
                '&tl={}'
                '&hl={}'
                '&dt=at'
                '&dt=bd'
                '&dt=ex'
                '&dt=ld'
                '&dt=md'
                '&dt=qca'
                '&dt=rw'
                '&dt=rm'
                '&dt=sos'
                '&dt=ss'
                '&dt=t'
                '&ssel=6'
                '&tsel=3'
                '&xid=45662847'
                '&kc=0'
                '&tk={}'
                '&q={}'
            ).format(_from, _to, _from, sign, key)
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
            return url,headers

        gtk = re.findall(r"tkk: *'(\d+.\d+)'", response.body.decode('utf-8'))[0]
        _from = response.meta.get('from')
        _to = response.meta.get('to')
        key = response.meta.get('key')
        sign = get_sign(gtk, key)
        url,headers = mk_url_headers(sign, key, _from, _to)
        meta = {}
        meta['proxy'] = self.proxy
        meta['to'] = _to
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('['):content.rfind(']')+1])
        d = {}
        d['translate'] = jsondata[0][0][0] # 翻译结果
        d['key']       = jsondata[0][0][1] # 需要被翻译的数据
        d['from']      = jsondata[8][3] # 来源语言
        d['to']        = response.meta.get('to')
        d['infos']     = jsondata
        # import pprint
        # pprint.pprint(d)
        yield d


# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/iWqolyAmzE'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
