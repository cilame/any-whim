# -*- coding: utf-8 -*-
# 挂钩中间件加载的处理，让通过“字符串”加载中间件的函数能够同时兼容用“类”加载中间件
import scrapy.utils.misc
import scrapy.utils.deprecate
_bak_load_object      = scrapy.utils.misc.load_object
_bak_update_classpath = scrapy.utils.deprecate.update_classpath
def _load_object(path_or_class):
    try: return _bak_load_object(path_or_class)
    except: return path_or_class
def _update_classpath(path_or_class):
    try: return _bak_update_classpath(path_or_class)
    except: return path_or_class
scrapy.utils.misc.load_object = _load_object
scrapy.utils.deprecate.update_classpath = _update_classpath

# 图片下载 item 中间件
import logging, hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class VImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        item['proxy'] = VSpider.proxy
        yield Request(item['src'], meta=item) 
    def file_path(self, request, response=None, info=None):
        url = request if not isinstance(request, Request) else request.url
        image_name = request.meta.get('image_name') # 使用 item中的 image_name 字段作为文件名进行存储，没有该字段则使用 url的 md5作为文件名存储
        image_name = re.sub(r'[/\\:\*"<>\|\?]', '_', image_name).strip()[:80] if image_name else hashlib.md5(url.encode()).hexdigest()
        return '%s/%s.jpg' % (request.meta.get('key'), image_name) # 生成的图片文件名字，此处可用/符号增加多级分类路径（路径不存在则自动创建），使用 image_name 请注意重名可能性。
    def item_completed(self, results, item, info): # 判断下载是否成功
        k, v = results[0]
        # if not k: logging.info('download fail {}'.format(item))
        # else:     logging.info('download success {}'.format(item))
        item.pop('proxy', None)
        item['image_download_stat'] = 'success' if k else 'fail'
        item['image_path'] = v['path'] if k else None # 保留文件名地址
        return item
















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
    proxy = 'http://127.0.0.1:8888'
    index = {}

    def start_requests(self):
        def mk_url_headers_body(page, key):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.google.com/_/VisualFrontendUi/data/batchexecute'
                '?rpcids=HoAMBc'
                '&f.sid=1484552913048631198'
                '&bl=boq_visualfrontendserver_20200214.01_p1'
                '&hl=en-US'
                '&authuser'
                '&soc-app=162'
                '&soc-platform=1'
                '&soc-device=1'
                '&_reqid=142196'
                '&rt=c'
            )
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "cookie": (
                    "DV=MzB0UiguEPQtwDWaKe0v0OimEEJmBddGUz1EEumeBAIAAAA; "
                    "NID=198=SU1N0X0TlV1FfnWH1NVNJ2OmHzx7hnM2Bb1Iwgkh-7h6wpDFwIsf8DK1vZOwU7G4ZaGc6bGca2ZsdoMbB8uhfezMREiX9T53Ldv0GOq-KXT3q9Z4Y18rDl5Coes2SoHfd69mtDk7XmmtFgi0z0s8Zh-GyRA02IPjbrMqZrSnv2k; "
                    "OTZ=5328196_24_24__24_; "
                    "1P_JAR=2020-02-18-03"
                ),
                "origin": "https://www.google.com",
                "referer": "https://www.google.com/",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
                "x-client-data": "CLO1yQEIhrbJAQiitskBCMG2yQEIqZ3KAQjiqMoBCMuuygEIyq/KAQjOsMoBCPe0ygEIjrrKAQ==",
                "x-goog-ext-190139975-jspb": "[\"ZZ\"]",
                "x-same-domain": "1"
            }
            body = {
                "f.req": "[[[\"HoAMBc\",\"[null,null,[" + str(page) + ",null,450,1,1280,[[\\\"m_jkppg-2ek_iM\\\",200,200,-2147352321]],[],[],null,null,null,534],\\\"\\\",\\\"\\\",null,null,null,null,null,null,\\\"\\\",null,null,null,null,null,null,null,null,null,null,null,null,\\\"\\\",null,null,null,[\\\"" + key + "\\\",\\\"\\\",null,\\\"\\\",\\\"\\\",\\\"\\\",\\\"\\\",\\\"\\\",\\\"\\\",null,null,\\\"\\\",\\\"\\\",\\\"\\\",\\\"\\\"]]\",null,\"generic\"]]]"
            }
            return url,headers,body

        keys = ['狗']
        for key in keys:
            for page in range(1, 80):
                url,headers,body = mk_url_headers_body(page, key)
                meta = {}
                meta['key'] = key
                meta['proxy'] = self.proxy
                r = Request(
                        url,
                        method   = 'POST',
                        headers  = headers,
                        body     = urlencode(body),
                        callback = self.parse,
                        meta     = meta,
                    )
                yield r
                break
            break

    def parse(self, response):
        key = response.meta.get('key')
        if key not in self.index: self.index[key] = 0

        e = r'''(https://encrypted[^"]+)\\[^\[]+\[\\"([^\\"]+)\\".*?rgb\(\d+,\d+,\d+\).*?http[^"]+\\",\\"([^"]+)\\'''
        s = map(lambda i:(i[0].replace('\\\\', '\\').encode().decode('unicode_escape'), i[1], i[2]), re.findall(e, response.body.decode()))

        for i in s:

            title = i[2] # 图片标题
            cache = i[0] # 缓存图片地址，下载成功率最高（小图）
            src   = i[1] # 原始地址，由于有些图片原始网站有问题，所以使用原始地址下载有一定的失败率（大图）

            self.index[key] += 1
            d = {}
            d['src'] = i[0] # 这里用了缓存地址下载，看你需求是否使用原始地址。
            d['title'] = i[2]
            d['index'] = self.index[key]
            d['key'] = key
            yield d
            break

# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/vjmKIYsbln'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        # 'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        'FEED_URI':                 filename,   # 下载数据到文件
        'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, cvs, xml, pickle, marshal
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多

        # 【中间件/管道配置】
        # 这里使用中间件的方式和项目启动很相似，我在头部打了补丁函数，现在管道配置的第一个值可以同时用字符串或类配置，突破了原版只能用字符串的限制。
        'IMAGES_STORE':             'image',      # 默认在该脚本路径下创建文件夹、下载图片(不解开 VImagePipeline 管道注释则该配置无效)
        'ITEM_PIPELINES': {
            VImagePipeline:         102,
        },
    })
    p.crawl(VSpider)
    p.start()