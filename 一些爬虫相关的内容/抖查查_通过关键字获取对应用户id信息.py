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
from urllib.parse import unquote, quote, urlencode

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers_body(key):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://api.douchacha.com/api/tiktok/search/user'
                '?ts=1596428038759'
                '&he=wo0KwrcTQN/ULyAKK3rTPsbAw7kULsbswrDJEMRAw5MPXsbp'
                '&sign=e8c1bb3181a69058'
            )
            url = quote_val(url)
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json;charset=UTF-8",
                "d-v": "NCw=",
                "dcc-href": "https://www.douchacha.com/searchdetail?from=DOUSearch&name=liuyixing198910",
                "dcc-r": "https://www.douchacha.com/uppoint",
                "Host": "api.douchacha.com",
                "Origin": "https://www.douchacha.com",
                "Pragma": "no-cache",
                "Referer": "https://www.douchacha.com/searchdetail?from=DOUSearch&name=liuyixing198910",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
            }
            body = "{\"page_no\":1,\"page_size\":10,\"params_data\":{\"keyword\":\""+str(key).strip()+"\",\"sort\":\"SCORE\"}}"
            return url,headers,body

        keys = []
        keys.append({'抖音号':'你好'})

        for key in keys:
            url,headers,body = mk_url_headers_body(key['抖音号'])
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = key
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = body,
                    callback = self.parse,
                    meta     = meta,
                )
            yield r
            break

    def parse(self, response):
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['data']['result']:
            d = response.meta.get('_plusmeta', {})
            # d["enterprise_verify_reason"]   = i.get("enterprise_verify_reason")
            # d["mcn_id"]                     = i.get("mcn_id")
            # d["province"]                   = i.get("province")
            # d["district"]                   = i.get("district")
            # d["country"]                    = i.get("country")
            # d["is_living"]                  = i.get("is_living")
            # d["city"]                       = i.get("city")
            # d["location"]                   = i.get("location")
            # d["user_tag"]                   = i.get("user_tag")
            # d["is_gov_media_vip"]           = i.get("is_gov_media_vip")           # 0
            # d["is_star"]                    = i.get("is_star")                    # 0
            # d["commerce_user_level"]        = i.get("commerce_user_level")        # 0
            # d["is_reset_user"]              = i.get("is_reset_user")              # 0
            # d["goods_count"]                = i.get("goods_count")                # 0
            # d["goods_video_count"]          = i.get("goods_video_count")          # 0
            # d["dongtai_count"]              = i.get("dongtai_count")              # 0
            # d["is_verified"]                = i.get("is_verified")                # 0
            # d["gender"]                     = i.get("gender")                     # 0
            # d["with_fusion_shop_entry"]     = i.get("with_fusion_shop_entry")     # 0
            # d["live_count"]                 = i.get("live_count")                 # 0
            # d["custom_verify"]              = i.get("custom_verify")
            # d["self_video_count"]           = i.get("self_video_count")           # 0
            # d["constellation"]              = i.get("constellation")              # 0
            # d["aweme_count"]                = i.get("aweme_count")                # 1
            # d["video_forward_total_count"]  = i.get("video_forward_total_count")  # 0
            # d["video_comment_total_count"]  = i.get("video_comment_total_count")  # 0
            # d["video_share_total_count"]    = i.get("video_share_total_count")    # 0
            # d["video_download_total_count"] = i.get("video_download_total_count") # 0
            # d["video_good_total_count"]     = i.get("video_good_total_count")     # 0
            # d["birthday"]                   = i.get("birthday")
            d["total_favorited"]            = i.get("total_favorited")            # 4
            d["following_count"]            = i.get("following_count")            # 214
            d["follower_count"]             = i.get("follower_count")             # 14
            d["favoriting_count"]           = i.get("favoriting_count")           # 1191
            # d["is_updating"]                = i.get("is_updating")                # False
            # d["update_complete"]            = i.get("update_complete")            # False
            # d["unique_id"]                  = i.get("unique_id")
            d["short_id"]                   = i.get("short_id")                   # 377793472
            d["user_id"]                    = i.get("user_id")                    # 75374513104
            d["last_update_time"]           = i.get("last_update_time")           # 1591895386000
            d["user_score"]                 = i.get("user_score")                 # 24.96433513834598
            d["signature"]                  = i.get("signature")                  # 先定一个能达到的小目标，比方说来句签名
            d["nickname"]                   = i.get("nickname")                   # <span style="color:red">PJTucker</span>–塔克
            d["share_url"]                  = i.get("share_url")
            # d["avatar_larger"]              = i.get("avatar_larger")              # https://p3-dy-ipv6.byteimg.com/img/tos-cn-i-0813/efff047fe29
            #                                                                       # 349f484d60a061d499d6a~c5_720x720.jpeg?from=4010531038
            # d["day7_inc"]                   = i.get("day7_inc")                   # {'change_aweme_count': '0', 'change_follower_count': '0', 'c
            #                                                                       # hange_total_favorited': '0', 'change_comment_count': '0', 'c
            #                                                                       # hange_share_count': '0'}
            # d["day30_inc"]                  = i.get("day30_inc")                  # {'change_aweme_count': '0', 'change_follower_count': '0', 'c
            #                                                                       # hange_total_favorited': '0', 'change_comment_count': '0', 'c
            #                                                                       # hange_share_count': '0'}
            print('------------------------------ split ------------------------------')
            import pprint
            pprint.pprint(d)
            yield d




# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'get_uids_{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/PYWKHeZrzj'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
        'DOWNLOAD_DELAY':           .05,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
