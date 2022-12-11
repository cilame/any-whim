# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

# scrapy(twisted) 对极少数的某些网站返回的不规范 headers 无法正常处理，这里只是补丁代码，丝毫不会影响到正常代码。
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

import re
import json, time
from urllib.parse import unquote, quote

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers_body(imgbitdata):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://graph.baidu.com/upload'
                '?uptime={}'
            ).format(int(time.time()*1000))
            url = quote_val(url)
            headers = {
                "Host": "graph.baidu.com",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
                "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryofv25hS8r5wg4hWQ",
            }
            body = b"""------WebKitFormBoundaryofv25hS8r5wg4hWQ
Content-Disposition: form-data; name="image"; filename="qq11qq.jpg"
Content-Type: image/jpeg

""".replace(b'\n', b'\r\n') + imgbitdata + b"""
------WebKitFormBoundaryofv25hS8r5wg4hWQ
Content-Disposition: form-data; name="tn"

pc
------WebKitFormBoundaryofv25hS8r5wg4hWQ
Content-Disposition: form-data; name="from"

pc
------WebKitFormBoundaryofv25hS8r5wg4hWQ
Content-Disposition: form-data; name="image_source"

PC_UPLOAD_MOVE
------WebKitFormBoundaryofv25hS8r5wg4hWQ--""".replace(b'\n', b'\r\n')
            return url,headers,body

        # 只需要读取图片的bit数据类型即可
        with open('qqqq.jpg', 'rb') as f:
            imgbitdata = f.read()

        url,headers,body = mk_url_headers_body(imgbitdata)
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
        jsondata = json.loads(response.body.decode('utf-8'))
        url = jsondata['data']['url']
        def mk_url_headers(url):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(url)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_info,
                meta     = meta,
            )
        yield r

    def parse_info(self, response):
        content = response.xpath('//script[contains(text(), "window.cardData")]').extract()[0]
        content = re.findall(r'window\.cardData ?= ?(.*?\}\]);', content)
        d = {}
        if content:
            for i in json.loads(content[0]):
                if i.get('cardName') == 'baike':
                    d = {**d, **i['tplData']}

        import pprint
        pprint.pprint(d)



# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/tlKgUOFsbc'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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