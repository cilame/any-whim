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
    # proxy = 'http://140.205.171.24:80'
    debug_break = False

    def start_requests(self):
        def mk_url_headers(key):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                '?page=1'
                '&n=2'
                '&group=class'
                '&p={}'
            ).format(key)
            url = quote_val(url)
            headers = {
                # "trpr-client-name": "mit-spider",
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        for key in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            url,headers = mk_url_headers(key)
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse,
                    meta     = meta,
                )
            yield r
            if self.debug_break: break

    def parse(self, response):
        for x in response.xpath('//body/div/div[2][@class="mp10"]'):
            d = {}
            d["href"]    = x.xpath('./div/a[@href]/@href')[0].extract() # [cnt:40] [len:11] /fam/254069
            d["zh_name"] = x.xpath('string(./div[1]/a[@href])')[0].extract()
            d["en_name"] = x.xpath('string(./div[2]/a[@href])')[0].extract()
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            # continue
            if '/fam/' in d['href']:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=fam'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/fam/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_fam_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break
            if '/gen/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=gen'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/gen/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_gen_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break
            if '/sp/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=sp'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/sp/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_sp_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break

    def parse_fam_page(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        count = jsondata["count"]
        nextstr = re.findall(r"href='([^']+)'", jsondata["nextstr"])[0]
        for page in range(1, int(count)+1):
            def mk_url_headers(page, nextstr):
                url = response.urljoin(nextstr)
                url = re.sub(r'page=(\d+)', 'page={}'.format(page), url)
                headers = {
                    # "trpr-client-name": "mit-spider",
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(page, nextstr)
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_gen_or_sp,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r
            if self.debug_break: break



    def parse_gen_or_sp(self, response):
        for x in response.xpath('//div[contains(@class, "item3")]'):
            d = {}
            d["href"] = x.xpath('./div[@class="mp10"]/div/a/@href')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["name"] = x.xpath('string(./div[@class="mp10"]/div/a)')[0].extract() # [cnt:2] [len:11] /gen/258751
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            # continue
            if '/gen/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=gen'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/gen/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_gen_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break
            if '/sp/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=sp'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/sp/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_sp_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break

    def parse_gen_page(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        count = jsondata["count"]
        nextstr = re.findall(r"href='([^']+)'", jsondata["nextstr"])[0]
        for page in range(1, int(count)+1):
            def mk_url_headers(page, nextstr):
                url = response.urljoin(nextstr)
                url = re.sub(r'page=(\d+)', 'page={}'.format(page), url)
                headers = {
                    # "trpr-client-name": "mit-spider",
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(page, nextstr)
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_gen,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r
            if self.debug_break: break

    def parse_gen(self, response):
        for x in response.xpath('//div[contains(@class, "item3")]'):
            d = {}
            d["href"] = x.xpath('./div[@class="mp10"]/div/a/@href')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["name"] = x.xpath('string(./div[@class="mp10"]/div/a)')[0].extract() # [cnt:2] [len:11] /gen/258751
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            # continue
            if '/gen/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=gen'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/gen/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_gen_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break
            if '/sp/' in d["href"]:
                def mk_url_headers(d):
                    url = (
                        'http://ppbc.iplant.cn/ashx/getphotopage.ashx'
                        '?t=0.25047715588424446'
                        '&n=1'
                        '&group=sp'
                        '&cid={}'
                        '&p='
                        '&m='
                    ).format(re.findall(r'/sp/(\d+)', d['href'])[0])
                    headers = {
                        # "trpr-client-name": "mit-spider",
                        "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                        "accept-language": "zh-CN,zh;q=0.9",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                    }
                    return url,headers
                url,headers = mk_url_headers(d)
                meta = {}
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        headers  = headers,
                        callback = self.parse_sp_page,
                        meta     = meta,
                    )
                yield r
                if self.debug_break: break


    def parse_sp_page(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        count = jsondata["count"]
        nextstr = re.findall(r"href='([^']+)'", jsondata["nextstr"])[0]
        for page in range(1, int(count)+1):
            def mk_url_headers(page, nextstr):
                url = response.urljoin(nextstr)
                url = re.sub(r'page=(\d+)', 'page={}'.format(page), url)
                headers = {
                    # "trpr-client-name": "mit-spider",
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(page, nextstr)
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_sp,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r
            if self.debug_break: break

    allcount = 0
    def parse_sp(self, response):
        for x in response.xpath('//div[contains(@class, "item3")]'):
            d = {}
            d["pid"] = x.xpath('./div[@class="item_t"]/div[@class="img"]/@pid')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["cno"] = x.xpath('./div[@class="item_t"]/div[@class="img"]/@cno')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["img_href"] = x.xpath('./div[@class="item_t"]/div/a/img/@src')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["name"] = x.xpath('./div[@class="item_t"]/div/a/img/@alt')[0].extract() # [cnt:2] [len:11] /gen/258751
            d["fullname"] = x.xpath('string(./div[@class="item_t"]/div/div[@class="namew fl"]/a)')[0].extract() # [cnt:2] [len:11] /gen/258751
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            self.allcount += 1
            yield d
        print('allcount', self.allcount)

















# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'ppbc_plant{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/nmVoRYNGBx'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        # 'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        'FEED_URI':                 filename,   # 下载数据到文件
        'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, csv, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           .1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
