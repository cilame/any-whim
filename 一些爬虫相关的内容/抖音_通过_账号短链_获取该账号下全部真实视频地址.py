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
                # 'https://v.douyin.com/J22geK9/'
                'https://v.douyin.com/J22oUBY/'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        # 使用账号短链接获取全部短视频本质上就是需要获取用户id，然后继续处理
        # 如果你能直接获取用户id，那么这个短链接就没有特别大的必要了，从parse函数直接往后处理即可，
        # 毕竟短链接有时效性，不如直接用用户id来得更加稳妥

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
        uid = re.findall(r'/share/[^/]+/(\d+)', u)[0]
        def mk_url_headers(uid, cursor=0):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.iesdouyin.com/web/api/v2/music/list/aweme/'
                '?music_id={}'
                '&count=9'
                '&cursor={}'
            ).format(uid, cursor)
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(uid)
        meta = {}
        meta['proxy'] = self.proxy
        meta['uid'] = uid
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_list,
                meta     = meta,
            )
        yield r

    def parse_list(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['aweme_list']:
            d = {}
            d["aweme_type"]     = i.get("aweme_type")     # 4
            # d["cha_list"]       = i.get("cha_list")       # None
            # d["video_labels"]   = i.get("video_labels")   # None
            # d["comment_list"]   = i.get("comment_list")   # None
            # d["label_top_text"] = i.get("label_top_text") # None
            # d["promotions"]     = i.get("promotions")     # None
            # d["image_infos"]    = i.get("image_infos")    # None
            # d["geofencing"]     = i.get("geofencing")     # None
            # d["video_text"]     = i.get("video_text")     # None
            # d["long_video"]     = i.get("long_video")     # None
            d["aweme_id"]       = i.get("aweme_id")       # 6850294134209629455
            d["desc"]           = i.get("desc")           # 教你们如何整理夹克 快快码起来#古着 #vintage #生活小技巧 #教学@抖音小助手
            # d["statistics"]     = i.get("statistics")     # {'aweme_id': '6850294134209629455', 'comment_count': 286, 'd
            #                                               # igg_count': 34000, 'play_count': 0, 'share_count': 1251, 'fo
            #                                               # rward_count': 9}
            # d["text_extra"]     = i.get("text_extra")     # [{'start': 40, 'end': 46, 'user_id': '6796248446', 'type': 0
            #                                               # , 'hashtag_name': '', 'hashtag_id': 0}, {'hashtag_id': 15904
            #                                               # 50288288775, 'start': 17, 'end': 20, 'type': 1, 'hashtag_nam
            #                                               # e': '古着'}, {'start': 21, 'end': 29, 'type': 1, 'hashtag_name
            #                                               # ': 'vintage', 'hashtag_id': 1585457315572750}, {'hashtag_id'
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            def mk_url_headers(vid):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/'
                    '?item_ids={}'
                ).format(vid)
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(d["aweme_id"])
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = d
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_real_vid,
                    meta     = meta,
                )
            yield r

        raise '测试代码只翻一页，所以，你如果想使用代码获取全量数据，请注意将该处代码注释掉！！！！'
        if jsondata['has_more']:
            uid = response.meta.get('uid')
            cursor = jsondata['cursor']
            def mk_url_headers(uid, cursor=0):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://www.iesdouyin.com/web/api/v2/music/list/aweme/'
                    '?music_id={}'
                    '&count=9'
                    '&cursor={}'
                ).format(uid, cursor)
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(uid, cursor)
            meta = {}
            meta['proxy'] = self.proxy
            meta['uid'] = uid
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_list,
                    meta     = meta,
                )
            yield r

    def parse_real_vid(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        vid = jsondata['item_list'][0]['video']['vid']
        def mk_url_headers(vid):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://aweme.snssdk.com/aweme/v1/play/' # 如果想要无水印，这行的 playwm 改成 play 就可以拿到无水印视频地址
                '?video_id={}'
                '&ratio=720p'
                '&line=0'
            ).format(vid)
            url = quote_val(url)
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
        meta['_plusmeta'] = response.meta.get('_plusmeta')
        meta['url_video_id'] = url
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_video_url,
                meta     = meta,
            )
        yield r

    def parse_video_url(self, response):
        middle_url = response.meta.get('url_video_id')
        video_url = response.xpath('//a/@href')[0].extract()
        d = response.meta.get('_plusmeta', {})
        d['video_url'] = video_url
        d['video_id_url'] = middle_url
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
    jobdir   = 'JOBDIR/yUjSkDhdLE'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
