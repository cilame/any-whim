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

    def start_requests(self):
        def mk_url_headers(page):
            pageinfo = (
                '{"comm":{"ct":24,'
                '"cv":0},'
                '"singerList":{"module":"Music.SingerListServer",'
                '"method":"get_singer_list",'
                '"param":{"area":-100,'
                '"sex":-100,'
                '"genre":-100,'
                '"index":-100,'
                '"sin":'+str(80*(page-1))+','
                '"cur_page":'+str(page)+'}}}'
            )
            import hashlib
            sign = hashlib.md5(('CJBPACrRuNy7'+pageinfo).encode()).hexdigest()
            url = (
                'https://u.y.qq.com/cgi-bin/musics.fcg'
                '?-=getUCGI12307520516540205'
                '&g_tk=5381'
                '&sign=zzalrmun5skwgav{}'
                '&loginUin=0'
                '&hostUin=0'
                '&format=json'
                '&inCharset=utf8'
                '&outCharset=utf-8'
                '&notice=0'
                '&platform=yqq.json'
                '&needNewCode=0'
                '&data={}'
            ).format(sign, pageinfo)
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        for page in range(1, 300):
            url,headers = mk_url_headers(page)
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse,
                    meta     = meta,
                )
            yield r
            # break

    def parse(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['singerList']['data']['singerlist']:
            d = {}
            d["country"]     = i.get("country")
            d["singer_id"]   = i.get("singer_id")   # 109253
            d["singer_name"] = i.get("singer_name") # Sparky Parks
            d["singer_mid"]  = i.get("singer_mid")  # 003bhMtM4fqf2i
            d["singer_pic"]  = i.get("singer_pic")  # http://y.gtimg.cn/music/photo_new/T001R150x150M000003bhMtM4f
                                                    # qf2i.webp
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d
            # break




# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/gLvwEsrcSD'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
