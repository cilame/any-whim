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
        def mk_url_headers_body(key):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://live.kuaishou.com/m_graphql'
            )
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "content-type": "application/json",
                "Cookie": (
                    "did=web_69f1ee03dc6ca2e8876f11e5fa03a6b2; "
                ),
                "Host": "live.kuaishou.com",
                "Origin": "https://live.kuaishou.com",
                "Pragma": "no-cache",
                "Referer": "https://live.kuaishou.com/search/?keyword=%E5%8D%8E%E4%B8%BA",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
            zstring = (
            'rVNNb8IwDL3zK3zgwCTED9ht2mFDQtoH44xCa9qIkIR8FKqp/33pKCwupWLTeqqf/WL72d'
            '55NCXMkZkkfynQFBz3bzU2Gm6w3CuT3sPcGS6zMQy9tfxs38HnAEAnlDs6s078MTS0I/1I'
            'AxDcuuYXYDKZgJJNGY/MYaZMOYsjAFyp8WwI6gNIGtI07QAfVisTwY47gZFtTRJZy2WdSb'
            'LtT0g1uOqsujpYWDR91X8Lcb0XHvdACqmDi6B9BLCCORZ3Z/EQWSnaxHDtuJKxMMpLZ0lS'
            'gDWT1FZCqD2BdK6cIkiHWrFe/yLnjBdonUG27V2JflF9mEmrYaJzh5IX4t/QrlbWoSFSh8'
            'tYGEHWsj0PUokWrAyE9nh2ngnuSoJ58u4N5V0+koXgqVyrVrbT6fTLof0qm/tw+AWjhZDJ'
            '1N8mbO0zml8uT87sO6avLNnQE8Anj9ZGGB70B4vP4m9r13IcYQJWg+oL'
            )
            import base64, zlib
            zstring = base64.b64decode(zstring)
            zstring = zlib.decompress(zstring,-15)
            string = zstring.decode("utf-8")
            body = {
                "operationName": "SearchOverviewQuery",
                "variables": {
                    "keyword": key,
                    "ussid": None
                },
                "query": string
            }
            body = json.dumps(body)
            return url,headers,body

        # 通过任意关键词在快手搜索到对应的账户id信息列表，按需求搜集即可
        key = '小米'

        url,headers,body = mk_url_headers_body(key)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = body,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['data']['pcSearchOverview']['list'][1]['list']:
            d = {}
            d["sex"]         = i.get("sex")         # M
            d["__typename"]  = i.get("__typename")  # User
            d["living"]      = i.get("living")      # False
            d["name"]        = i.get("name")        # 成哥的苹果二手精品店
            d["_id"]         = i.get("id")          # V15005391313  ##################### 这个字段就是账户ID
            d["description"] = i.get("description") # 感谢快手官方提供的绿色平台！感谢每一次热门！售后:15005391313诚信：12年手机实体卖场安心:官方认证快
                                                    # 手号放心:7天包退三个月质保位置:临沂市兰山区临西三路与红旗路交汇东50米路南
            d["counts"]      = i.get("counts")      # {'fan': '궪.쳏w', 'follow': '궪궬궬', 'photo': '궪궬ꫝ', '__typename
                                                    # ': 'CountInfo'}
            d["avatar"]      = i.get("avatar")      # https://tx2.a.yximgs.com/uhead/AB/2020/01/12/13/BMjAyMDAxMTI
                                                    # xMzI5MzFfNTQ2ODkxNzYyXzJfaGQ0MDJfNjcw_s.jpg
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
    jobdir   = 'JOBDIR/ljnZgCDvbi'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
