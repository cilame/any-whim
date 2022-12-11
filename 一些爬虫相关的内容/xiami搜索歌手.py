# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

# from twisted.internet.ssl import AcceptableCiphers # 当请求出现 ssl(dh key too small) 异常时，可以尝试解该处注释
# from scrapy.core.downloader import contextfactory
# contextfactory.DEFAULT_CIPHERS = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT:!DH')

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

    def start_requests(self):
        def mk_url_headers(singer_name):
            search_info = (
                '{"key":"' +singer_name+ '",'
                '"pagingVO":{"page":1,'
                '"pageSize":30}}'
            )
            import hashlib
            xm_sg_tk = 'd2614a8c68c19a3224f3516286db35d1_1592899912140'
            sign = xm_sg_tk.split('_')[0] + '_xmMain_' + '/api/search/searchSongs_' + search_info
            sign = hashlib.md5(sign.encode()).hexdigest()
            url = (
                'https://www.xiami.com/api/search/searchSongs'
                '?_q={}'
                '&_s={}'
            ).format(search_info, sign)
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = quote_val(url)
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "cookie": (
                    "xm_sg_tk.sig=ixs52oEBXd6kB5SYHoNhsgV2kXz6uZtTenA4u-fhCvw; "
                    "xm_sg_tk={}; "
                ).format(xm_sg_tk),
                "pragma": "no-cache",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
            }
            return url,headers

        # keys = []
        # with open('./singer.json', encoding='utf-8') as f:
        #     for i in f:
        #         if i.strip():
        #             keys.append(i.strip())
        keys = ['韩红']

        for idx, key in enumerate(keys):
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
            break

    def parse(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['result']['data']['songs']:
            d = {}
            d["artistVOs"]        = i.get("artistVOs")        # [{'artistId': 2099989996, 'artistStringId': 'nmSuiY95973', '
                                                              # artistName': '蔡徐坤', 'alias': 'Kun', 'gender': None, 'artistL
                                                              # ogo': None, 'isMusician': None, 'countLikes': None, 'isFavor
                                                              # ': None, 'rewardSchemaUrl': None}]
            d["singerVOs"]        = i.get("singerVOs")        # [{'artistId': 2099989996, 'artistStringId': 'nmSuiY95973', '
                                                              # artistName': '蔡徐坤', 'alias': 'Kun', 'gender': 'M', 'artistLo
                                                              # go': 'http://pic.xiami.net/images/artistlogo/42/158528038536
                                                              # 42.jpg', 'isMusician': False, 'countLikes': None, 'isFavor':
                                                              #  None, 'rewardSchemaUrl': None}]
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
    jobdir   = 'JOBDIR/kiCYjoVAmJ'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
