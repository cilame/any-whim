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

    # 快手抓取需要获取登录的cookie信息，最最关键的两个cookie参数如下，有了这两个才能获取到内容
    # 还是稍微有点麻烦的。
    cookie = (
        "did=web_69f1ee03dc6ca2e8876f11e5fa03a6b2; "
        "kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAaCxgdF_o_O7x8N8z8AkUsOmeN1gNgPUHOXMNzpY6azNABjMGhZbolZ5RJz4EcebGIsUQIGI_UXcE2F4SGWWm-dEBjve44g7ngYvwsUtVUl7Sj22fq04ahnIeJYD7AYjtEX19powUvuj6LhQKSEHCjgKH-qevGrgVuY_LZifULn_tW8A_jWyvETV5jsXQvFuz673AN2spr2-XjKEiga4H-caEoJNhwQ4OUDtgURWN6k9Xgm8PSIgiFzjrY3Fy9qGTFqChRFunkF2xIB_HfGkNMC-hp5KfUooBTAB; "
    )

    def start_requests(self):
        def mk_url_headers_body(principalId, pcursor=None):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://live.kuaishou.com/m_graphql'
            )
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "content-type": "application/json",
                "Cookie": self.cookie,
                "Host": "live.kuaishou.com",
                "Origin": "https://live.kuaishou.com",
                "Pragma": "no-cache",
                "Referer": "https://live.kuaishou.com/profile/huaweicorp",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
            zstring = (
            'hVPLTsMwELz3K3zgUKR+Qa+VgEoIAQWuaHGWZFW/6kdKQP13HIgdp4L2ZM9oPTv78C6g7Z'
            'gJb4L4FWLlHnpifmEsKU4GxLpaso2PqF6wC8ODddoWDNdB+SVbK3/JvmasVJpPNErFBctC'
            'SXLBBqVfxV8xluJ+7oJaHGjGgkObAWNU5Su04MFmqEBiBq+vvjNYUIfh3IPnTaxo1ScfOK'
            'OdxyTEdYv22YoEwXjSanaU3QjoYpArnO0CCPJdxiFrnLAzfVTHgLV614UqB4+1tt3fZcYh'
            '1JtgW2phTNanymAba71Bq89bacA9YnUPfDsQ/RiuAzo3YPwwT1DP/pQ5DINzPnvPvfJNkG'
            '8KSIxdnXR8r+32afRc2I+zf6EK9X3sdg4nWfedH9GGPjFBCXVcSuBJQQZH/G4sdjpOoWN7'
            'C0hbTKa1Et2VFkLv0a5ArbSUmBfGoojvWrxBqptEepLoPEiTyqLKN6m3ZeDP3pebU5Hr9+'
            'mFcH/M3UZLx9zUy4mJ/v91sLhPFuroT/0rfX4XJuRhdvgG'
            )
            import base64, zlib
            zstring = base64.b64decode(zstring)
            zstring = zlib.decompress(zstring,-15)
            string = zstring.decode("utf-8")
            body = {
                "operationName": "publicFeedsQuery",
                "variables": {
                    "principalId": principalId,
                    "pcursor": pcursor,
                    "count": 24
                },
                "query": string
            }
            body = json.dumps(body)
            return url,headers,body

        # 通过账户ID，获取到该账户下所有的视频，然后进而获取到全部的视频内容。
        principalId = "huaweicorp" # 通过用户的ID获取所有视频内容

        url,headers,body = mk_url_headers_body(principalId)
        meta = {}
        meta['proxy'] = self.proxy
        meta['principalId'] = principalId
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
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['data']['publicFeeds']['list']:
            d = {}
            d["imgUrls"]                = i.get("imgUrls")                # []
            d["imgSizes"]               = i.get("imgSizes")               # []
            d["height"]                 = i.get("height")                 # 480
            d["width"]                  = i.get("width")                  # 852
            d["magicFace"]              = i.get("magicFace")              # None
            d["musicName"]              = i.get("musicName")              # None
            d["location"]               = i.get("location")               # None
            d["relativeHeight"]         = i.get("relativeHeight")         # None
            d["useVideoPlayer"]         = i.get("useVideoPlayer")         # True
            d["_type"]                  = i.get("type")                   # work
            d["liked"]                  = i.get("liked")                  # False
            d["onlyFollowerCanComment"] = i.get("onlyFollowerCanComment") # False
            d["workType"]               = i.get("workType")               # video
            d["__typename"]             = i.get("__typename")             # VideoFeed
            d["expTag"]                 = i.get("expTag")                 # 1_a/0_null
            d["timestamp"]              = i.get("timestamp")              # 1573374011627
            d["_id"]                    = i.get("id")                     # 3xd6nbfrm4c53bc
            d["caption"]                = i.get("caption")                # 想静静时，轻敲两下 #HUAWEIFreeBuds3
            d["counts"]                 = i.get("counts")                 # {'displayView': '3599', 'displayLike': '74', 'displayComment
                                                                          # ': '13', '__typename': 'VideoCountInfo'}
            d["thumbnailUrl"]           = i.get("thumbnailUrl")           # https://tx2.a.yximgs.com/upic/2019/11/10/16/BMjAxOTExMTAxNjI
                                                                          # wMTBfODk0NjgyNjVfMTkzOTYzNzk3MDlfMl8z_B2a4e86dec3a8920cd4bac
                                                                          # c6f3618b887.jpg?di=7ae7e06b&bp=10004
            d["poster"]                 = i.get("poster")                 # https://tx2.a.yximgs.com/upic/2019/11/10/16/BMjAxOTExMTAxNjI
                                                                          # wMTBfODk0NjgyNjVfMTkzOTYzNzk3MDlfMl8z_B2a4e86dec3a8920cd4bac
                                                                          # c6f3618b887.jpg?di=7ae7e06b&bp=10004
            d["user"]                   = i.get("user")                   # {'id': 'huaweicorp', 'eid': '3xsxizdk9tx8gx2', 'name': '华为',
                                                                          #  'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2020/07/20/16/
                                                                          # BMjAyMDA3MjAxNjAxMzdfODk0NjgyNjVfMl9oZDg3NF83NDI=_s.jpg', '_
                                                                          # _typename': 'User'}
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            def mk_url_headers_body(principalId, photoId):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://live.kuaishou.com/m_graphql'
                )
                url = quote_val(url)
                headers = {
                    "accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "content-type": "application/json",
                    "Cookie": self.cookie,
                    "Host": "live.kuaishou.com",
                    "Origin": "https://live.kuaishou.com",
                    "Pragma": "no-cache",
                    "Referer": "https://live.kuaishou.com/profile/huaweicorp",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
                }
                zstring = (
                'KyxNLapUCM5ILEoNSExPDQRxNVQKijLzkjMLEnM8U6wUgkuAvHQdBZWCjPySfISIpkI1l4'
                'JCWmpqilOlZ4oGih5kE3QU4BphRkC0KigklxYVpeaVhOcXZUNFFBQKchIrQ4tyoLz4+JLK'
                'gtS8xNxUsEAtF4ZgLVctAA=='
                )
                import base64, zlib
                zstring = base64.b64decode(zstring)
                zstring = zlib.decompress(zstring,-15)
                string = zstring.decode("utf-8")

                body = {
                    "operationName": "SharePageQuery",
                    "variables": {
                        "photoId": photoId,
                        "principalId": principalId
                    },
                    "query": string
                }
                body = json.dumps(body)
                return url,headers,body
            principalId = response.meta.get('principalId')
            url,headers,body = mk_url_headers_body(principalId, d["_id"])
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = body,
                    callback = self.parse_video_url,
                    meta     = meta,
                )
            yield r

        raise '测试代码只翻一页，所以，你如果想使用代码获取全量数据，请注意将该处代码注释掉！！！！'
        pcursor = jsondata['data']['publicFeeds'].get('pcursor')
        if pcursor != 'no_more':
            def mk_url_headers_body(principalId, pcursor=None):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://live.kuaishou.com/m_graphql'
                )
                url = quote_val(url)
                headers = {
                    "accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "content-type": "application/json",
                    "Cookie": self.cookie,
                    "Host": "live.kuaishou.com",
                    "Origin": "https://live.kuaishou.com",
                    "Pragma": "no-cache",
                    "Referer": "https://live.kuaishou.com/profile/huaweicorp",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
                }
                zstring = (
                'hVPLTsMwELz3K3zgUKR+Qa+VgEoIAQWuaHGWZFW/6kdKQP13HIgdp4L2ZM9oPTv78C6g7Z'
                'gJb4L4FWLlHnpifmEsKU4GxLpaso2PqF6wC8ODddoWDNdB+SVbK3/JvmasVJpPNErFBctC'
                'SXLBBqVfxV8xluJ+7oJaHGjGgkObAWNU5Su04MFmqEBiBq+vvjNYUIfh3IPnTaxo1ScfOK'
                'OdxyTEdYv22YoEwXjSanaU3QjoYpArnO0CCPJdxiFrnLAzfVTHgLV614UqB4+1tt3fZcYh'
                '1JtgW2phTNanymAba71Bq89bacA9YnUPfDsQ/RiuAzo3YPwwT1DP/pQ5DINzPnvPvfJNkG'
                '8KSIxdnXR8r+32afRc2I+zf6EK9X3sdg4nWfedH9GGPjFBCXVcSuBJQQZH/G4sdjpOoWN7'
                'C0hbTKa1Et2VFkLv0a5ArbSUmBfGoojvWrxBqptEepLoPEiTyqLKN6m3ZeDP3pebU5Hr9+'
                'mFcH/M3UZLx9zUy4mJ/v91sLhPFuroT/0rfX4XJuRhdvgG'
                )
                import base64, zlib
                zstring = base64.b64decode(zstring)
                zstring = zlib.decompress(zstring,-15)
                string = zstring.decode("utf-8")
                body = {
                    "operationName": "publicFeedsQuery",
                    "variables": {
                        "principalId": principalId,
                        "pcursor": pcursor,
                        "count": 24
                    },
                    "query": string
                }
                body = json.dumps(body)
                return url,headers,body

            principalId = response.meta.get('principalId')
            url,headers,body = mk_url_headers_body(principalId, pcursor)
            meta = {}
            meta['proxy'] = self.proxy
            meta['principalId'] = principalId
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = body,
                    callback = self.parse,
                    meta     = meta,
                )
            yield r

    def parse_video_url(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        # import pprint
        # pprint.pprint(jsondata, depth= None )
        video_url = jsondata['data']['feedById']['currentWork']['playUrl']
        print(video_url)






# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/ENvnyGeqoC'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
