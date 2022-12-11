# https://shenzhen.qfang.com/
# qfang网，深圳二手房数据抓取，直接执行即可测试（代码含有 wzws_cid 参数解密）
# 需要安装 scrapy 和 pyexecjs 库，最好还安装了 nodejs 软件。
# parse 和 parse2 均为中间解密解析处理，多执行调试几次即可明白原理。



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
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://shenzhen.qfang.com/sale'
                '?utm_source=baidu'
                '&utm_medium=cpc'
                '&utm_term=PC-SZ-sale-105959286977-深圳二手房'
                '&renqun_youhua=717391'
            )
            url = quote_val(url)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "shenzhen.qfang.com",
                "Pragma": "no-cache",
                "Referer": "https://shenzhen.qfang.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        meta['proxy'] = self.proxy
        meta['origurl'] = url
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        enc = response.xpath('//script[contains(text(), "sojson.v5")]/text()').extract()
        if enc:
            encstring = enc[0]
            # 这里的js算法非常简单，以下四行代码就解决了。如果细看内部算法，可以用纯python实现，
            # 就不用依赖 pyexecjs 和 nodejs 之类的模拟 js 执行的环境了。这里我懒得看了。
            import execjs
            jscode = encstring.replace('_0x10ace8;', '_0x10ace8;return _0x35ace3;') + ';function test(){ return _0x33f22a(); }'
            ctx = execjs.compile(jscode)
            url = 'https://shenzhen.qfang.com/WZWSRELw==?'+ctx.call('test').split('=?')[-1]

            currcookie = response.headers.to_unicode_dict()['set-cookie']
            def mk_url_headers(url, currcookie):
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Cookie": (
                        currcookie
                    ),
                    "Host": "shenzhen.qfang.com",
                    "Pragma": "no-cache",
                    "Referer": "https://shenzhen.qfang.com/",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(url, currcookie)
            meta = {}
            meta['proxy'] = self.proxy
            meta['dont_redirect'] = True
            meta['handle_httpstatus_list'] = [302]
            meta['origurl'] = response.meta.get('origurl')
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse2,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r
        else:
            raise "unknown error."

    def parse2(self, response):
        origurl = response.meta.get('origurl')
        relcookie = response.headers.to_unicode_dict()['set-cookie']
        def mk_url_headers(url, relcookie):
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": (
                    relcookie
                ),
                "Host": "shenzhen.qfang.com",
                "Pragma": "no-cache",
                "Referer": "https://shenzhen.qfang.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(origurl, relcookie)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_info,
                meta     = meta,
                dont_filter = True,
            )
        yield r

    def parse_info(self, response):
        class none:pass
        none.extract = lambda:None
        for x in response.xpath('//li/div[2][contains(@class, "list-main")]'):
            d = {}
            d["title"]          = (x.xpath('./div/a[1][@class="house-title fl"]/@title') or [none])[0].extract()      # [cnt:30] [len:30] 龙光玖龙台 玖龙台 高层四房看花园 全明通透可看房 交通方便
            d["href"]           = (x.xpath('./div/a[1][@class="house-title fl"]/@href') or [none])[0].extract()       # [cnt:30] [len:41] /sale/101371311?insource=sale_...
            d["href_7"]         = (x.xpath('./div/a[1][@class="school fl"]/@href') or [none])[0].extract()            # [cnt:30] [len:19] /school/detail/1575
            d["str_list"]       = x.xpath('string(./div[@class="list-main-header clearfix"])')[0].extract()           # [cnt:30] [len:42]  龙光玖龙台 玖龙台 高层四房看花园 全明通透可看房 交通方...
            d["str_house"]      = x.xpath('string(./div/a[1][@class="house-title fl"])')[0].extract()                 # [cnt:30] [len:30] 龙光玖龙台 玖龙台 高层四房看花园 全明通透可看房 交通方便
            d["str_house_1"]    = x.xpath('string(./div[@class="house-metas clearfix"])')[0].extract()                # [cnt:30] [len:40]   4室2厅 104㎡ 精装 高层(共36层) 南 201
            d["str_meta"]       = x.xpath('string(./div/p[2][@class="meta-items"])')[0].extract()                     # [cnt:30] [len:4] 104㎡
            d["str_meta_1"]     = x.xpath('string(./div/p[4][@class="meta-items"])')[0].extract()                     # [cnt:30] [len:10]  高层(共36层)
            d["str_meta_2"]     = x.xpath('string(./div/p[6][@class="meta-items"])')[0].extract()                     # [cnt:30] [len:14]  2017年-2019年建
            d["str_house_2"]    = x.xpath('string(./div[@class="house-location clearfix"])')[0].extract()             # [cnt:30] [len:18]   光明区- 公明- 龙光玖龙台            d["str_house_3"]    = x.xpath('string(./div[@class="house-tags clearfix"])')[0].extract()                 # [cnt:30] [len:36]  深圳市光明新区光明小学 距离6号线(光明线)凤凰城站约42...
            d["str_school"]     = x.xpath('string(./div/a[1][@class="school fl"])')[0].extract()                      # [cnt:30] [len:11] 深圳市光明新区光明小学
            if "str_all"        in d: d["str_all"       ] = re.sub(r'\s+',' ',d["str_all"]).strip()
            if "str_list"       in d: d["str_list"      ] = re.sub(r'\s+',' ',d["str_list"]).strip()
            if "str_house"      in d: d["str_house"     ] = re.sub(r'\s+',' ',d["str_house"]).strip()
            if "str_house_1"    in d: d["str_house_1"   ] = re.sub(r'\s+',' ',d["str_house_1"]).strip()
            if "str_iconfont"   in d: d["str_iconfont"  ] = re.sub(r'\s+',' ',d["str_iconfont"]).strip()
            if "str_meta"       in d: d["str_meta"      ] = re.sub(r'\s+',' ',d["str_meta"]).strip()
            if "str_meta_1"     in d: d["str_meta_1"    ] = re.sub(r'\s+',' ',d["str_meta_1"]).strip()
            if "str_meta_2"     in d: d["str_meta_2"    ] = re.sub(r'\s+',' ',d["str_meta_2"]).strip()
            if "str_house_2"    in d: d["str_house_2"   ] = re.sub(r'\s+',' ',d["str_house_2"]).strip()
            if "str_school"     in d: d["str_school"    ] = re.sub(r'\s+',' ',d["str_school"]).strip()
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
    jobdir   = 'JOBDIR/NxApOcIPrS'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
