# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import quote,unquote
import base64

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # use my create cookie in headers
    }

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url):
                url = unquote(url)
                for i in re.findall('=([^=&]+)',url):
                    url = url.replace(i,'{}'.format(quote(i)))
                return url
            url = (
                'https://www.99lib.net/article/12001.htm'
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
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):

        '''
        该网站的顺序混肴其实都藏在请求页面的head标签的其中一个meta里面
        里面的content就藏有标签顺序，不过这个顺序是经过base64加密的，简单解密一下
        然后再用正则进行分割就找到顺序下标的部分了，不过这时的顺序下标还不算完整，
        还需要通过这个网站的一个算法进行调整才能获取到正常的顺序结构。这个算法就藏在js里面
        需要调试一会儿才能拿到。

        **值得注意的是，对于两种文章有不同的加密算法，分别对应相应类型的网页
        1/   https://www.99lib.net/book/9622/345609.htm    这种网页使用 book 函数解密
        2/   https://www.99lib.net/article/12000.htm       这种网页使用 article 函数解密
        '''

        def book(response):
            k = response.xpath('//meta[@name="client"]/@content')[0].extract()
            v = base64.b64decode(k).decode()
            e = list(map(int,re.split('[A-Z]+%',v)))
            c = {}
            j = 0
            for i in range(len(e)):
                if e[i] < 3:
                    c[e[i]] = i
                    j += 1
                else:
                    c[e[i] - j] = i
                    j += 2
            v = response.xpath('//*[@id="content"]/div')
            for i,realidx in sorted(c.items()):
                d = v[realidx].extract()
                yield d
            
        def article(response):
            k = response.xpath('//meta[@name="client"]/@content')[0].extract()
            v = base64.b64decode(k).decode()
            e = list(map(int,re.split('[A-Z]+%',v)))
            c = {}
            j = 0
            for i in range(len(e)):
                if e[i] < 5:
                    c[e[i]] = i
                    j += 1
                else:
                    c[e[i] - j] = i
            v = response.xpath('//*[@id="content"]/div')
            for i,realidx in sorted(c.items()):
                d = v[realidx].extract()
                yield d

        for i in article(response):
            print(i)
            print('----------- split ------------')
