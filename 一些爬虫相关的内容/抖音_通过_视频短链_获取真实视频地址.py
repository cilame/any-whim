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
            url = (
                'https://v.douyin.com/Jecfuhe/'
            )
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
        meta['dont_redirect'] = True,
        meta['handle_httpstatus_list'] = [302]
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        u = response.xpath('//a/@href')[0].extract() if response.status == 302 else response.url
        vid = re.findall(r'video/(\d+)/', u)[0]
        def mk_url_headers(vid):
            url = (
                'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/'
                '?item_ids={}'
            ).format(vid)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(vid)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_real_vid,
                meta     = meta,
            )
        yield r

    def parse_real_vid(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        vid = jsondata['item_list'][0]['video']['vid']
        def mk_url_headers(vid):
            url = (
                'https://aweme.snssdk.com/aweme/v1/play/' # 如果想要无水印，这行的 playwm 改成 play 就可以拿到无水印视频地址
                '?video_id={}'
                '&ratio=720p'
                '&line=0'
            ).format(vid)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                # 如果想要使用无水印的地址直接观看，那么就必须使用手机的 headers 才能在浏览器上直接播放
                # 这里使用的是 chrome 手机模式获取到的 headers 。
                "user-agent": "User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(vid)
        meta = {}
        meta['proxy'] = self.proxy
        meta['dont_redirect'] = True,
        meta['handle_httpstatus_list'] = [302]
        meta['url_video_id'] = url
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_video_url,
                meta     = meta,
            )
        yield r

    def parse_video_url(self, response):
        # middle_url 虽然直接就能下载了，不过会有两种情况，如果这个 url 里面带有 playwm 那么可以直接下载（浏览器直接观看）
        # 如果 url 里面的 playwm 换成了 play 那么就需要在下载头里面增加一个手机模式的 headers 信息才能下载
        # video_url 能直接下载，不过每次通过 middle_url 跳转到的 video_url 都是不定的，该地址可能会过期。

        # 简单说：
        # middle_url 固定，不过下载无水印视频有点麻烦。
        # video_url 不固定，不过在一段时间内就是真实视频地址。
        middle_url = response.meta.get('url_video_id')
        video_url = response.xpath('//a/@href')[0].extract()
        print(middle_url)
        print(video_url)




# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/wrJEOpCyvB'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
