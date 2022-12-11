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
    IMAGES_STORE = None
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        VImagePipeline.IMAGES_STORE = settings.get('IMAGES_STORE')
    def get_media_requests(self, item, info):
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        item = item.copy()
        item['download_timeout'] = 180 # 下载单张图片的时间限制
        yield Request(item['src'], headers=headers, meta=item) 
    def file_path(self, request, response=None, info=None):
        url = request if not isinstance(request, Request) else request.url
        image_name = request.meta.get('image_name') # 使用 item中的 image_name 字段作为文件名进行存储，没有该字段则使用 url的 md5作为文件名存储
        image_name = re.sub(r'[/\\:\*"<>\|\?]', '_', image_name).strip()[:80] if image_name else hashlib.md5(url.encode()).hexdigest()
        return '%s.jpg' % image_name # 生成的图片文件名字，此处可用/符号增加多级分类路径（路径不存在则自动创建），使用 image_name 请注意重名可能性。
    def item_completed(self, results, item, info): # 判断下载是否成功
        k, v = results[0]
        item['image_download_stat'] = 'success' if k else 'fail'
        item['image_path'] = os.path.join(VImagePipeline.IMAGES_STORE, v['path']).replace('\\', '/') if k else None # 保留文件名地址
        if not k: logging.info('download fail {}'.format(item))
        else:     logging.info('download success {}'.format(item))
        return item



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
        def mk_url_headers(key):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://baike.baidu.com/item/{}'
            ).format(key)
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        # keys = ['卡迪根威尔士柯基犬']

        keys = []
        with open('./dog_cat.txt', encoding='utf-8') as f:
            for i in f:
                if i.strip():
                    keys.append(i.strip())

        for key in keys:
            url,headers = mk_url_headers(key)
            meta = {}
            meta['proxy'] = self.proxy
            meta['key'] = key
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse,
                    meta     = meta,
                )
            yield r

    def parse(self, response):
        lemmaId = re.findall(r'newLemmaId: *"(\d+)"', response.body.decode('utf-8'))[0]
        key = response.meta.get('key')
        def mk_url_headers(key, lemmaId):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://baike.baidu.com/pic/{}/{}'
            ).format(key, lemmaId)
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        url,headers = mk_url_headers(key, lemmaId)
        meta = {}
        meta['proxy'] = self.proxy
        meta['_plusmeta'] = {'key': key}
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_pic_page_list,
                meta     = meta,
            )
        yield r

    def parse_pic_page_list(self, response):
        _meta = response.meta.get('_plusmeta')
        class none:pass
        none.extract = lambda:None
        for x in response.xpath('//div[contains(@class, "album-item")]'):
            d = {}
            d["find_key"]  = (x.xpath('./div/div/a[1][@class="pic album-cover"]/@title') or [none])[0].extract() # [cnt:8] [len:4] 词条图片
            d["href"]      = (x.xpath('./div/div/a[1][@class="pic album-cover"]/@href') or [none])[0].extract()  # [cnt:8] [len:113] /pic/%E9%87%91%E6%AF%9B%E5%AF%...
            def mk_url_headers(d):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2))), url)
                url = response.urljoin(d['href'])
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(d)
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = {**_meta, **d} # keys word transfer
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_pic_list,
                    meta     = meta,
                )
            yield r

    count = 0
    def parse_pic_list(self, response):
        _meta = response.meta.get('_plusmeta')
        s = response.xpath('//script[contains(text(), "PictureDialog.getInstance()")]').extract()[0]
        content = re.findall('albums:([^\n]+)', s)[0]
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for key in jsondata:
            for pics in jsondata[key].get('pictures') or []:
                imginfo = max(pics['sizes'].items(), key=lambda x:(x[1].get('height') or 0)*(x[1].get('width') or 0))
                img_url = imginfo[1]['url']
                d = _meta.copy()
                d['src'] = img_url
                self.count += 1
                print(self.count, img_url)
                yield d


# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/dyFrHzBbvu'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
        # 【中间件/管道配置】
        # 这里使用中间件的方式和项目启动很相似，我在头部打了补丁函数，现在管道配置的第一个值可以同时用字符串或类配置，突破了原版只能用字符串的限制。
        'IMAGES_STORE':             'image',      # 默认在该脚本路径下创建文件夹、下载【图片】(不解开 VImagePipeline 管道注释则该配置无效)
        'FILES_STORE':              'file',       # 默认在该脚本路径下创建文件夹、下载【文件】(不解开 VFilePipeline 管道注释则该配置无效)
        'MEDIAS_STORE':             'media',      # 默认在该脚本路径下创建文件夹、下载【媒体】(不解开 VVideoPipeline 管道注释则该配置无效)
        'ITEM_PIPELINES': {
            # VPipeline:              101,        # 普通的中间件使用(解开即可测试，如需魔改，请在脚本顶部找对应的类进行自定义处理)
            VImagePipeline:         102,        # 图片下载中间件，item 带有 src 字段则以此作为图片地址下载到 IMAGES_STORE 地址的文件夹内
            # VFilePipeline:          103,        # 文件下载中间件，item 带有 src 字段则以此作为文件地址下载到 FILES_STORE 地址的文件夹内
            # VVideoPipeline:         104,        # 视频下载中间件，item 带有 src 字段则以此作为媒体地址下载到 MEDIAS_STORE 文件夹内
            # VMySQLPipeline:         105,        # MySql 插入中间件，具体请看类的描述
            # VOssPipeline:           106,        # 将本地数据上传到 OSS 空间的管道模板，注意修改模板内 process_item 函数来指定上传文件地址
            # VMoreSavePipeline:      107,        # 如果需要同时存储多种格式的本地文件，可以使用这个模板(例如同时存储 jsonline 和 csv 文件)
        },
    })
    p.crawl(VSpider)
    p.start()
