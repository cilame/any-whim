# python3
# pip install cryptography scrapy
# 直接执行本代码即可单脚本运行 scrapy 以测试接口

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
def get_encryptor(key, iv=None, mode='aes'):
    if mode == 'aes': alg = algorithms.AES
    if mode == 'des': alg = algorithms.TripleDES
    algoer = alg(key) #若要使用DES这里改成TripleDES
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
def decode_alg(data, key, iv, mode): return get_encryptor(key, iv, mode).decrypt(base64.b64decode(data))
def encode_alg(data, key, iv, mode): return base64.b64encode(get_encryptor(key, iv, mode).encrypt(data))
decode_des = lambda data, key, iv: decode_alg(data, key, iv, 'des')
decode_aes = lambda data, key, iv: decode_alg(data, key, iv, 'aes')
encode_aes = lambda data, key, iv: encode_alg(data, key, iv, 'aes')
encode_des = lambda data, key, iv: encode_alg(data, key, iv, 'des')

def get_enc_dec_conf(s):
    import re
    def parse_evaljs(s):
        x = r"\}\(('(?:[^'\\]|\\.)*') *, *(\d+) *, *(\d+) *, *'((?:[^'\\]|\\.)*)'\.split\('\|'\) *, *(\d+) *, *(\{\})"
        p, a, c, k, e, d = re.findall(x, s)[0]
        p, a, c, e, k, d = eval(p), int(a), int(c), int(e), k.split('|'), {}
        def evaljs_code(p, a, c, k, e, d):
            def e(c):
                x = '' if c < a else e(int(c/a))
                c = c % a
                return x + (chr(c + 29) if c > 35 else '0123456789abcdefghijklmnopqrstuvwxyz'[c])
            for i in range(c): d[e(i)] = k[i] or e(i)
            return re.sub(r'\b(\w+)\b', lambda e: d.get(e.group(0)) or e.group(0), p)
        return evaljs_code(p, a, c, k, e, d)
    js = parse_evaljs(s)
    conf = {}
    e_aes = re.findall(r'AES\.decrypt\(data,([^,\)]+),([^,\)]+)\);', js)[0]
    e_des = re.findall(r'DES\.decrypt\(data,([^,\)]+),([^,\)]+)\);', js)[0]
    conf['decode_aes_k'] = re.findall('const {}="([^"]+)"'.format(e_aes[0]), js)[0]
    conf['decode_aes_v'] = re.findall('const {}="([^"]+)"'.format(e_aes[1]), js)[0]
    conf['decode_des_k'] = re.findall('const {}="([^"]+)"'.format(e_des[0]), js)[0]
    conf['decode_des_v'] = re.findall('const {}="([^"]+)"'.format(e_des[1]), js)[0]
    # 在解密的代码内找到解密的算法，一共有三种内层加密情况：AES/DES/无 。这里根据js代码分析对算法自动选择。
    d_cry = re.findall(r'([a-zA-Z0-9]+)\.encrypt\(param,([^,\)]+),([^,\)]+)\);', js) 
    if d_cry:
        d_cry = d_cry[0]
        conf['encode_cry_k'] = re.findall('const {}="([^"]+)"'.format(d_cry[1]), js)[0]
        conf['encode_cry_v'] = re.findall('const {}="([^"]+)"'.format(d_cry[2]), js)[0]
        conf['cry_type'] = d_cry[0]
    conf['appid'] = re.findall(r"var appId='([^']+)';", js)[0]
    conf['_pkey'] = re.findall(r"([a-zA-Z0-9]+):param", js)[0]
    return conf

def decode_return(data, conf):
    import json, base64, hashlib
    _my_md5   = lambda string:hashlib.md5(string.encode()).hexdigest()
    aes_k = _my_md5(conf['decode_aes_k'])[16:].encode()
    aes_v = _my_md5(conf['decode_aes_v'])[:16].encode()
    des_k = _my_md5(conf['decode_des_k'])[:16].encode()
    des_v = _my_md5(conf['decode_des_v'])[24:].encode()
    des_k = des_k + des_k[8:]
    data = decode_aes(data, aes_k, aes_v)
    data = decode_des(data, des_k, des_v)
    data = json.loads(base64.b64decode(data).decode())
    return data

def encode_postbody(city, conf):
    appid = conf['appid']
    _pkey = conf['_pkey']
    import json, time, hashlib, base64
    _my_md5 = lambda string:hashlib.md5(string.encode()).hexdigest()
    _my_dumps = lambda obj:json.dumps(obj,ensure_ascii=False,separators=(',',':'))
    appId = appid
    method = "GETDATA"
    timestamp = int(time.time()*1000)
    clienttype = "WEB"
    _object = {"city":city}
    secret = _my_md5(appId+method+str(timestamp)+clienttype+_my_dumps(_object))
    info = _my_dumps({
        "appId":appId,
        "method":method,
        "timestamp":timestamp,
        "clienttype":clienttype,
        "object":_object,
        "secret":secret,
    })
    binfo = base64.b64encode(info.encode())
    def _my_enc(data):
        def enc_aes(data):
            aes_k = _my_md5(conf['encode_cry_k'])[16:].encode()
            aes_v = _my_md5(conf['encode_cry_v'])[:16].encode()
            return encode_aes(binfo, aes_k, aes_v).decode()
        def enc_des(data):
            des_k = _my_md5(conf['encode_cry_k'])[:16].encode()
            des_v = _my_md5(conf['encode_cry_v'])[24:].encode()
            des_k = des_k + des_k[8:]
            return encode_des(binfo, des_k, des_v).decode()
        if conf.get('cry_type') == 'AES': return enc_aes(data)
        if conf.get('cry_type') == 'DES': return enc_des(data)
        if not conf.get('cry_type'): return data.decode()
    return {_pkey: _my_enc(binfo)}








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
                'https://www.aqistudy.cn/html/city_realtime.php'
                '?v=2.3'
            )
            url = quote_val(url)
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
        content = response.body.decode()
        url = response.urljoin(re.findall(r'src="(\.\./js/encrypt_[^"]+)', content)[0])
        def mk_url_headers(url):
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(url)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_js,
                meta     = meta,
            )
        yield r

    def parse_js(self, response):
        conf = get_enc_dec_conf(response.body.decode())
        def mk_url_headers_body(city):
            url = (
                'https://www.aqistudy.cn/apinew/aqistudyapi.php'
            )
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            body = encode_postbody(city, conf)
            return url,headers,body
        url,headers,body = mk_url_headers_body('杭州') # 前面的请求是算法参数的收集，这里包装的请求是通过收集到的算法参数 conf 加密请求参数，发起最终请求。
        meta = {}
        meta['proxy'] = self.proxy
        meta['conf'] = conf
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
        conf = response.meta.get('conf')
        data = decode_return(response.body.decode(), conf)
        import pprint
        # pprint.pprint(conf)
        pprint.pprint(data)





# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/lPqLaXSGBd'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
