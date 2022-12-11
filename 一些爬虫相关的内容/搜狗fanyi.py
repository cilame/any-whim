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
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.sogou.com/'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        # 接口只需要在这里添加需要翻译的key即可。
        key = '''
Il pleure dans mon cœur
Comme il pleut sur la ville ;
Quelle est cette langueur
Qui pénètre mon cœur ?
 
Ô bruit doux de la pluie
Par terre et sur les toits !
Pour un cœur qui s'ennuie
Ô le chant de la pluie !
 
Il pleure sans raison
Dans ce cœur qui s'écœure.
Quoi ! nulle trahison ? ...
Ce deuil est sans raison.
 
C'est bien la pire peine
De ne savoir pourquoi
Sans amour et sans haine
Mon cœur a tant de peine! '''

        keys = []
        keys.append(key)

        target_lang = "zh-CHS" ############# 要翻译成什么语言，请替换这个参数，例如翻译成英语这里换成 en
        for idx, key in enumerate(keys):
            url,headers = mk_url_headers()
            meta = {}
            meta['proxy'] = self.proxy
            meta['key'] = key
            meta['target_lang'] = target_lang
            meta['idx'] = idx
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r

            # if idx == 10000:
            #     break

    def parse(self, response):
        SNUID = re.findall('SNUID=[^;]+', response.headers.to_unicode_dict()['set-cookie'])[0]
        CONFIG = {}
        CONFIG['secretCode'] = re.findall(r'"secretCode" *: *(\d+)', response.body.decode())[0]
        CONFIG['uuid'] = re.findall(r'"uuid" *: *"([^"]+)"', response.body.decode())[0]
        target_lang = response.meta.get('target_lang')
        idx = response.meta.get('idx')
        def mk_url_headers_body(SNUID, CONFIG, target_lang):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://fanyi.sogou.com/reventondc/translateV2'
            )
            url = quote_val(url)
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": (
                    SNUID
                ),
                "Host": "fanyi.sogou.com",
                "Origin": "https://fanyi.sogou.com",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
            }
            import hashlib
            _from = "auto"
            _to   = target_lang
            text  = response.meta.get('key').strip()
            skey  = str(CONFIG['secretCode'])
            body = {
                "from": _from,
                "to": _to,
                "text": text,
                "client": "wap",
                "fr": "browser_pc",
                "pid": "sogou-dict-vr",
                "dict": "true",
                "word_group": "true",
                "second_query": "true",
                "uuid": CONFIG['uuid'],
                "needQc": "1",
                "s": hashlib.md5((_from + _to + text + skey).encode()).hexdigest()
            }
            return url,headers,body
        url,headers,body = mk_url_headers_body(SNUID, CONFIG, target_lang)
        meta = {}
        meta['proxy'] = self.proxy
        meta['target_lang'] = target_lang
        meta['key'] = response.meta.get('key')
        meta['idx'] = response.meta.get('idx')
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = urlencode(body),
                callback = self.parse_info,
                meta     = meta,
            )
        yield r

    def parse_info(self, response):
        key = response.meta.get('key')
        target_lang = response.meta.get('target_lang')
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        # import pprint
        # pprint.pprint(jsondata, depth= None )
        translate = jsondata['data']['translate']['dit']
        language  = jsondata['data']['detect']['language']
        d = {}
        d['key'] = key
        d['translate'] = translate
        d['target_lang'] = target_lang
        d['language']= language
        d['content'] = jsondata
        # import pprint
        # pprint.pprint(d, depth= None )
        print(response.meta.get('idx'), key, translate)
        yield d


# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/KbgArfavnw'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
