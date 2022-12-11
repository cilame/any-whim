# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

# 以下补丁代码：用于预防有人可能会用 pythonw 执行 scrapy 单脚本时可能会出现的编码问题，如果直接用 python 执行该处则有无皆可。
# import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 以下补丁代码：用于预防处理 “scrapy(twisted) 对极少数的某些网站返回的不规范 headers 无法处理” 的异常情况
def lineReceived(self, line):
    if line[-1:] == b'\r': line = line[:-1]
    if self.state == u'STATUS': self.statusReceived(line); self.state = u'HEADER'
    elif self.state == u'HEADER':
        if not line or line[0] not in b' \t':
            if self._partialHeader is not None:
                _temp = b''.join(self._partialHeader).split(b':', 1)
                name, value = _temp if len(_temp) == 2 else (_temp[0], b'')
                self.headerReceived(name, value.strip())
            if not line: self.allHeadersReceived()
            else: self._partialHeader = [line]
        else: self._partialHeader.append(line)
import twisted.web._newclient
twisted.web._newclient.HTTPParser.lineReceived = lineReceived
# 以下补丁代码：解决 idna 库过于严格，导致带有下划线的 hostname 无法验证通过的异常
import idna.core
_check_label_bak = idna.core.check_label
def check_label(label):
    try: return _check_label_bak(label)
    except idna.core.InvalidCodepoint: pass
idna.core.check_label = check_label

import re
import json
from urllib.parse import unquote, quote

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'
    debug_break = False

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx'
                '?typeId=1'
                '&brandId=0'
                '&fctId=0'
                '&seriesId=0'
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
        meta['_plusmeta'] = {} # keys word transfer
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        _meta = response.meta.get('_plusmeta') or {}
        for x in response.xpath('//li'):
            d = {}
            d["href"] = x.xpath('./h3/a[@href]/@href')[0].extract() # [cnt:238] [len:20] /price/brand-94.html
            d["lv1"]  = x.xpath('string(.)')[0].extract()                       # [cnt:238] [len:7] 众泰(437)
            if "lv1" in d: d["lv1"] = re.sub(r'\s+',' ',d["lv1"])
            brandId = re.findall(r'/brand-(\d+)\.html', d['href'])[0]
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            # continue
            def mk_url_headers(brandId):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx'
                    '?typeId=1'
                    '&brandId={}'
                    '&fctId=0'
                    '&seriesId=0'
                ).format(brandId)
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers

            # # 好像是奥迪
            # if '33' == brandId:
            #     url,headers = mk_url_headers(brandId)
            #     meta = {}
            #     meta['proxy'] = self.proxy
            #     meta['_plusmeta'] = d
            #     r = Request(
            #             url,
            #             headers  = headers,
            #             callback = self.parse_list,
            #             meta     = meta,
            #         )
            #     yield r
            #     if self.debug_break: break

            brandId = re.findall(r'/brand-(\d+)\.html', d['href'])[0]
            url,headers = mk_url_headers(brandId)
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = d
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_list,
                    meta     = meta,
                )
            yield r
            if self.debug_break: break

    def parse_list(self, response):
        _meta = response.meta.get('_plusmeta')
        for x in response.xpath('//li/dl'):
            lv2 = None
            for i in x.xpath('./dt|./dd'):
                if i.root.tag == 'dt':
                    lv2 = i.xpath('string(.)')[0].extract()
                if i.root.tag == 'dd':
                    d = {}
                    d["href"] = response.urljoin(i.xpath('./a/@href')[0].extract())
                    d['lv1'] = _meta['lv1']
                    d["lv2"] = lv2
                    d["lv3"] = i.xpath('string(.)')[0].extract()
                    # print(d)
                    # yield d
                    def mk_url_headers(url):
                        headers = {
                            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                            "accept-language": "zh-CN,zh;q=0.9",
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                        }
                        return url,headers
                    url,headers = mk_url_headers(d["href"])
                    meta = {}
                    meta['proxy'] = self.proxy
                    meta['_plusmeta'] = d
                    r = Request(
                            url,
                            headers  = headers,
                            callback = self.parse_info,
                            meta     = meta,
                        )
                    yield r
                    if self.debug_break: break


    def parse_info(self, response):
        d = response.meta.get('_plusmeta')
        d['price'] = response.xpath('//span[@class="font-arial"]/text()')[0].extract()
        def mk_url_headers():
            url = response.xpath('//a[contains(@href, "/pic/") and contains(text(), "图片")]/@href')[0].extract()
            url = response.urljoin(url)
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
        meta['_plusmeta'] = d
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_pic_list_first,
                meta     = meta,
            )
        yield r

    def parse_pic_list_first(self, response):
        _meta = response.meta.get('_plusmeta')
        for x in response.xpath('//div[contains(text(), "按分类：")]/parent::*//li'):
            d = _meta.copy()
            d['href'] = response.urljoin(x.xpath('./a/@href')[0].extract())
            d['type'] = x.xpath('./a/text()')[0].extract()
            number = int(re.findall(r'\( *(\d+) *张\)', x.xpath('./a/span/text()')[0].extract())[0])
            pages = int(number/60) if number%60==0 else int(number/60)+1
            def mk_url_headers(url, page):
                if page != 1:
                    url = re.sub(r'\.html', '-p{}.html'.format(page), url)
                headers = {
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            for page in range(1, pages+1):
                url,headers = mk_url_headers(d['href'], page)
                meta = {}
                meta['proxy'] = self.proxy
                meta['_plusmeta'] = d
                meta['page'] = page
                meta['pages'] = pages
                meta['number'] = number
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_pic_list,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break
            if self.debug_break: break

    count = 0
    def parse_pic_list(self, response):
        # print('page/pages:', response.meta.get('page'), response.meta.get('pages'))
        _meta = response.meta.get('_plusmeta')
        for x in response.xpath('//div[contains(@class, "uibox-con")]/ul/li'):
            d = _meta.copy()
            d['lv4'] = x.xpath('./a/@title')[0].extract()
            d['img_src'] = response.urljoin(x.xpath('./a/img/@src')[0].extract())
            d['img_src_ori'] = re.sub(r'/\d+x\d+_', '/0x0_', d['img_src'])
            self.count += 1
            yield d
        print(self.count)








# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/jlCYVnxErv'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        'FEED_URI':                 filename,   # 下载数据到文件
        'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, csv, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        'DOWNLOAD_DELAY':           .1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
