# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import unquote, quote

class parse16:
    def __init__(self, bytes):
        self.pos = 0
        self.bytes = bytes
    def get_int16(self):
        ret = int.from_bytes(self.bytes[self.pos:self.pos+2], 'little'); self.pos += 2
        return ret
    def get_ustring(self):
        R = [self.get_int16() for i in range(len(self.bytes)//2)]
        R = ''.join([chr(i) if i < 256 else (b'\\u' + hex(i)[2:].encode()).decode('unicode_escape') for i in R])
        return R

class unmarshal:
    def __init__(self, bytes):
        self.pos = 0
        self.bytes = bytes
    def get_int32(self):
        ret = int.from_bytes(self.bytes[self.pos:self.pos+4], 'little'); self.pos += 4
        return ret
    def get_int16(self):
        ret = int.from_bytes(self.bytes[self.pos:self.pos+2], 'little'); self.pos += 2
        return ret
    def get_int8(self):
        ret = int.from_bytes(self.bytes[self.pos:self.pos+1], 'little'); self.pos += 1
        return ret
    def get_bytes(self):
        len = self.get_int16()
        ret = self.bytes[self.pos:self.pos+len]; self.pos += len
        return ret
    def get_string(self):
        return ''.join([chr(self.get_int8()) for i in range(self.get_int16())])
    def get_ustring(self):
        len = self.get_int32()
        ret = self.bytes[self.pos:self.pos+len]; self.pos += len
        return parse16(ret).get_ustring()

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):

        # 通过视频pid获取全部的弹幕
        pid = '15012_2464519401_39811675_1585621082589'

        def mk_url_headers(pid):
            import time
            url = (
                'https://www.yy.com/video/replay/comments'
                '?pid={}'
                '&offset=0'
                '&limit=30'
                '&sort=desc'
                '&n={}'
                '&pageContext='
            ).format(pid, int(time.time()*1000))
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(pid)
        meta = {}
        meta['proxy'] = self.proxy
        meta['pid'] = pid
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_danmu,
                meta     = meta,
            )
        yield r

    def parse_danmu(self, response):
        s = unmarshal(response.body)
        s.get_int32()
        for i in range(s.get_int32()):
            s.get_string()
            s.get_int32()
            s.get_int32()
            a = unmarshal(s.get_bytes())
            l = [a.get_int32(), a.get_int32(), a.get_int16(), a.get_int32(), a.get_int32(), a.get_int32(), a.get_bytes()][-1]
            u = unmarshal(l)
            c = [u.get_int32(), u.get_ustring()][-1]
            f = [u.get_int32(), u.get_int32(), u.get_ustring()][-1]
            try:
                f = etree.HTML(f).xpath('//txt/@data')[0]
            except:
                pass
            d = {}
            d['nickname']= c
            d['text']= f
            d['ctime'] = time.strftime("%Y%m%d_%H%M%S", time.localtime(s.get_int32()))
            d['pid'] = response.meta.get('pid')
            s.get_int32()
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d
        # 获取弹幕总数，因为该处的参数 s 与上面的弹幕解析耦合，所以不能将上面部分单独分割出去做一个函数，另写一个类似的函数即可。
        info = {}
        for i in range(s.get_int32()):
            v = s.get_string()
            info[v] = s.get_string()
        total = int(info['total'])
        pages = int(total/30) if total%30==0 else int(total/30)+1
        for page in range(1, pages):
            def mk_url_headers(url, page):
                url = re.sub('&offset=[^&]+', '&offset={}'.format(page*30), url)
                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(response.url, page)
            meta = {}
            meta['proxy'] = self.proxy
            meta['pid'] = response.meta.get('pid')
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_danmu_page,
                    meta     = meta,
                )
            yield r

    def parse_danmu_page(self, response):
        s = unmarshal(response.body)
        s.get_int32()
        for i in range(s.get_int32()):
            s.get_string()
            s.get_int32()
            s.get_int32()
            a = unmarshal(s.get_bytes())
            l = [a.get_int32(), a.get_int32(), a.get_int16(), a.get_int32(), a.get_int32(), a.get_int32(), a.get_bytes()][-1]
            u = unmarshal(l)
            c = [u.get_int32(), u.get_ustring()][-1]
            f = [u.get_int32(), u.get_int32(), u.get_ustring()][-1]
            try:
                f = etree.HTML(f).xpath('//txt/@data')[0]
            except:
                pass
            d = {}
            d['nickname']= c
            d['text']= f
            d['ctime'] = time.strftime("%Y%m%d_%H%M%S", time.localtime(s.get_int32()))
            d['pid'] = response.meta.get('pid')
            s.get_int32()
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d



# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/QnhawTYsHN'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, cvs, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
