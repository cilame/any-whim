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
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers(author_id):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://haokan.baidu.com/author/{}'
            ).format(author_id)
            url = quote_val(url)
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
            return url,headers

        author_id = '1663051666056650'

        url,headers = mk_url_headers(author_id)
        meta = {}
        meta['proxy'] = self.proxy
        meta['author_id'] = author_id
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_first_page,
                meta     = meta,
            )
        yield r

    def parse_first_page(self, response):
        content = response.xpath('//script[@id="_page_data"]').extract()[0].split('document.querySelector', 1)[0]
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        # import pprint
        # pprint.pprint(jsondata, depth= 4 )
        for i in jsondata['video']['results']:
            d = {}
            d["tplName"] = i.get("tplName") # video
            d["_type"]   = i.get("type")    # video
            d["_content"] = i.get("content") # {'vid': '13606937375490730500', 'publish_time': '06月05日', 't
                                             # itle': '开车高速发生追尾，原因是你不知道自己车辆，有效制动距离是多少', 'cover_src': 'https
                                             # ://pic.rmb.bdstatic.com/bjh/video/2c770ea8ce72f84bbe50835f21
                                             # df73f9.jpeg@s_0,w_460,h_260,q_80', 'cover_src_pc': 'https://
                                             # pic.rmb.bdstatic.com/bjh/video/2c770ea8ce72f84bbe50835f21df7
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d

        if jsondata['video']['has_more']:
            ctime = jsondata['video']['ctime']
            def mk_url_headers(ctime, author_id):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://haokan.baidu.com/author/{}'
                    '?_format=json'
                    '&rn=16'
                    '&ctime={}'
                    '&_api=1'
                ).format(author_id, ctime)
                url = quote_val(url)
                headers = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(ctime, response.meta.get('author_id'))
            meta = {}
            meta['proxy'] = self.proxy
            meta['author_id'] = response.meta.get('author_id')
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_next_page,
                    meta     = meta,
                )
            yield r


    def parse_next_page(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['data']['response']['results']:
            d = {}
            d["tplName"] = i.get("tplName") # video
            d["_type"]   = i.get("type")    # video
            d["_content"] = i.get("content") # {'vid': '13606937375490730500', 'publish_time': '06月05日', 't
                                             # itle': '开车高速发生追尾，原因是你不知道自己车辆，有效制动距离是多少', 'cover_src': 'https
                                             # ://pic.rmb.bdstatic.com/bjh/video/2c770ea8ce72f84bbe50835f21
                                             # df73f9.jpeg@s_0,w_460,h_260,q_80', 'cover_src_pc': 'https://
                                             # pic.rmb.bdstatic.com/bjh/video/2c770ea8ce72f84bbe50835f21df7
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d

        if jsondata['data']['response']['has_more']:
            ctime = jsondata['data']['response']['ctime']
            def mk_url_headers(ctime, author_id):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://haokan.baidu.com/author/{}'
                    '?_format=json'
                    '&rn=16'
                    '&ctime={}'
                    '&_api=1'
                ).format(author_id, ctime)
                url = quote_val(url)
                headers = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(ctime, response.meta.get('author_id'))
            meta = {}
            meta['proxy'] = self.proxy
            meta['author_id'] = response.meta.get('author_id')
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_next_page,
                    meta     = meta,
                )
            yield r




# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/uJfhXDBFTw'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
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
