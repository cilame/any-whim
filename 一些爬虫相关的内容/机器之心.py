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
                'https://www.jiqizhixin.com/categories/basic'
            )
            url = quote_val(url)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "www.jiqizhixin.com",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        meta['proxy'] = self.proxy
        meta['page'] = 1
        meta['dont_redirect'] = True,
        meta['handle_httpstatus_list'] = list(range(400, 420))
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_cookie,
                meta     = meta,
            )
        yield r

    def parse_cookie(self, response):
        set_cookie = response.headers.to_unicode_dict()['set-cookie']
        _Synced_session = re.findall(r'(_Synced_session=[^; ]+)', set_cookie)[0]
        ahoy_visitor = re.findall(r'(ahoy_visitor=[^; ]+)', set_cookie)[0]
        ahoy_visit = re.findall(r'(ahoy_visit=[^; ]+)', set_cookie)[0]
        ncoockie = '{}; {}; {}'.format(ahoy_visitor, ahoy_visit, _Synced_session)
        csrf_token = response.xpath('//meta[@name="csrf-token"]/@content').extract()[0]

        def mk_url_headers_body(ncoockie, csrf_token, cursor=''):
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.jiqizhixin.com/graphql'
            )
            url = quote_val(url)
            headers = {
                "accept": "*/*",
                "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "content-type": "application/json",
                "Cookie": ncoockie,
                "Host": "www.jiqizhixin.com",
                "Origin": "https://www.jiqizhixin.com",
                "Pragma": "no-cache",
                "Referer": "https://www.jiqizhixin.com/categories/basic",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                "X-CSRF-Token": csrf_token
            }
            body = "{\"operationName\":\"category\",\"variables\":{\"cursor\":\"" + cursor.strip() + "\",\"count\":12,\"title\":\"basic\",\"filterTags\":[]},\"query\":\"query category($title: String!, $count: Int, $cursor: String, $filterTags: [String]) {\\n  category(category_name: $title, first: $count, after: $cursor, filter_tags: $filterTags) {\\n    edges {\\n      node {\\n        ...ArticleInfo\\n        __typename\\n      }\\n      __typename\\n    }\\n    pageInfo {\\n      ...PageInfo\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment PageInfo on PageInfo {\\n  endCursor\\n  hasNextPage\\n  __typename\\n}\\n\\nfragment ArticleInfo on Article {\\n  ...ArticleSimple\\n  category_name\\n  category_path\\n  author {\\n    name\\n    id\\n    avatar_url\\n    path\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ArticleSimple on Article {\\n  id\\n  path\\n  title\\n  cover_image_url\\n  published_at\\n  likes_count\\n  comments_count\\n  description\\n  __typename\\n}\\n\"}"
            return url,headers,body
        url,headers,body = mk_url_headers_body(ncoockie, csrf_token)
        meta = {}
        meta['proxy'] = self.proxy
        meta['page'] = 1
        meta['csrf_token'] = csrf_token
        meta['ahoy_visitor'] = ahoy_visitor
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = body,
                callback = self.parse,
                meta     = meta,
                dont_filter = True,
            )
        yield r

    def parse(self, response):
        set_cookie = response.headers.to_unicode_dict()['set-cookie']
        _Synced_session = re.findall(r'(_Synced_session=[^; ]+)', set_cookie)[0]
        # ahoy_visitor = re.findall(r'(ahoy_visitor=[^; ]+)', set_cookie)[0]
        ahoy_visitor = response.meta.get('ahoy_visitor')
        ahoy_visit = re.findall(r'(ahoy_visit=[^; ]+)', set_cookie)[0]
        ncoockie = '{}; {}; {}'.format(ahoy_visitor, ahoy_visit, _Synced_session)
        content = response.body.decode("utf-8",errors="strict")
        jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
        for i in jsondata['data']['category']['edges']:
            d = {}
            d["__typename"] = i.get("__typename") # ArticleEdge
            d["node"]       = i.get("node")       # {'__typename': 'Article', 'category_name': '入门', 'category_p
                                                  # ath': '/categories/basic', 'author': {'name': '机器之心', 'id': 
                                                  # 'User/b6ef5e00-e24f-44ea-9404-78e24df29424', 'avatar_url': '
                                                  # https://cdn.jiqizhixin.com/assets/avatars/anonymous-3-fb31ad
                                                  # 35511be5a49c496964c9d2190933420699e44988a3401765d28949a1f8.j
            # print('------------------------------ split ------------------------------')
            # import pprint
            # pprint.pprint(d)
            # yield d
            def mk_url_headers(path):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = response.urljoin(path)
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(d['node']['path'])
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = d['node']
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_info,
                    meta     = meta,
                )
            yield r

        cursor = jsondata['data']['category']['pageInfo']['endCursor']
        print('curr page:', response.meta.get('page'), cursor)
        if jsondata['data']['category']['pageInfo']['hasNextPage']:
            def mk_url_headers_body(ncoockie, csrf_token, cursor=''):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
                url = (
                    'https://www.jiqizhixin.com/graphql'
                )
                url = quote_val(url)
                headers = {
                    "accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "content-type": "application/json",
                    "Cookie": ncoockie,
                    "Host": "www.jiqizhixin.com",
                    "Origin": "https://www.jiqizhixin.com",
                    "Pragma": "no-cache",
                    "Referer": "https://www.jiqizhixin.com/categories/basic",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "X-CSRF-Token": csrf_token
                }
                body = "{\"operationName\":\"category\",\"variables\":{\"cursor\":\"" + cursor.strip() + "\",\"count\":12,\"title\":\"basic\",\"filterTags\":[]},\"query\":\"query category($title: String!, $count: Int, $cursor: String, $filterTags: [String]) {\\n  category(category_name: $title, first: $count, after: $cursor, filter_tags: $filterTags) {\\n    edges {\\n      node {\\n        ...ArticleInfo\\n        __typename\\n      }\\n      __typename\\n    }\\n    pageInfo {\\n      ...PageInfo\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment PageInfo on PageInfo {\\n  endCursor\\n  hasNextPage\\n  __typename\\n}\\n\\nfragment ArticleInfo on Article {\\n  ...ArticleSimple\\n  category_name\\n  category_path\\n  author {\\n    name\\n    id\\n    avatar_url\\n    path\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ArticleSimple on Article {\\n  id\\n  path\\n  title\\n  cover_image_url\\n  published_at\\n  likes_count\\n  comments_count\\n  description\\n  __typename\\n}\\n\"}"
                return url,headers,body

            csrf_token = response.meta.get('csrf_token')
            url,headers,body = mk_url_headers_body(ncoockie, csrf_token, cursor)
            meta = {}
            meta['proxy'] = self.proxy
            meta['page'] = response.meta.get('page') + 1
            meta['csrf_token'] = csrf_token
            meta['ahoy_visitor'] = ahoy_visitor
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = body,
                    callback = self.parse,
                    meta     = meta,
                    dont_filter = True,
                )
            yield r

    def parse_info(self, response):
        d = response.meta.get('_plusmeta') or {}
        def parse_content_type(content, types=['utf-8','gbk']):
            for tp in types:
                try:    return tp, content.decode(tp)
                except: pass
            etp = types[:]
            try:
                import chardet
                tp = chardet.detect(content)['encoding']
                if tp not in etp: etp.append(tp); return tp, content.decode(tp)
            except: pass
            import re # 有些网站明明就是gbk或utf-8编码但就是解析失败，所以用errors=ignore模式下中文数量来兜底编码格式
            utf8len = len(re.findall('[\u4e00-\u9fa5]', content.decode('utf-8', errors='ignore')[:4096]))
            gbklen  = len(re.findall('[\u4e00-\u9fa5]', content.decode('gbk', errors='ignore')[:4096]))
            gtp = 'gb18030' if gbklen > utf8len else 'utf-8'
            err = 'encoding not in :[{}]. Guess encoding is [{},errors:ignore]'.format(','.join(etp), gtp)
            return err, content.decode(gtp, errors='ignore')

        content = [i.xpath('string(.)')[0].extract().strip() for i in response.xpath('//div[@id="js-article-content"]/p')]
        content = [i for i in content if i.strip()]
        tp, html = parse_content_type(response.body)
        # d['html'] = html
        d['content'] = content
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
    jobdir   = 'JOBDIR/ZAwFspMxYr'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

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
        'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
