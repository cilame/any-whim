# -*- coding: utf-8 -*-
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
def get_encryptor(key, iv=None):
    algoer = algorithms.AES(key) #若要使用DES这里改成TripleDES
    mode   = modes.CBC(iv)       #模式若是ecb则为 modes.ECB(), 其余模式均为一个参数 mode.***(iv)
    cipher = Cipher(algoer, mode, backend=default_backend())
    def enc(bitstring):
        padder    = padding.PKCS7(algoer.block_size).padder()
        bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()
    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata     = decryptor.update(bitstring) + decryptor.finalize()
        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
        return unpadder.update(ddata) + unpadder.finalize()
    class f:pass
    f.encrypt = enc
    f.decrypt = dec
    return f


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
                'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list'
                '?pg=0'
                '&pgsz=15'
                '&total=0'
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
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        content = get_encryptor(b'jo8j9wGw%6HbxfFn', b'0123456789ABCDEF').decrypt(base64.b16decode(response.body.upper()))
        jsondata = json.loads(content)
        for i in jsondata['data']['list']:
            d = {}
            d["QY_SRC_TYPE"]    = i.get("QY_SRC_TYPE")    # 0
            d["IS_FAKE"]        = i.get("IS_FAKE")        # 0
            d["RN"]             = i.get("RN")             # 15
            d["QY_FR_NAME"]     = i.get("QY_FR_NAME")     # 郑志强
            d["QY_REGION"]      = i.get("QY_REGION")      # 440100
            d["QY_REGION_NAME"] = i.get("QY_REGION_NAME") # 广东省-广州市
            d["OLD_CODE"]       = i.get("OLD_CODE")       # 190437587
            d["QY_NAME"]        = i.get("QY_NAME")        # 广州市自来水工程有限公司
            d["COLLECT_TIME"]   = i.get("COLLECT_TIME")   # 1477106420000
            d["QY_ORG_CODE"]    = i.get("QY_ORG_CODE")    # 91440101190437587Y
            d["QY_ID"]          = i.get("QY_ID")          # 6C6C6D6A6C6B6E6E6C6C696B6D6568686D6C
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
    jobdir   = 'JOBDIR/DxzlGiIqmv'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
