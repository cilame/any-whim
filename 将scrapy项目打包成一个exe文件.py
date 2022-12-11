# pyinstaller 打包 scrapy 项目成一个 exe 文件的方式

modules = (
    'scrapy',
    'email',
    'twisted',
    'queuelib',
    'sqlite3',
)

import os
import sys
d = os.path.join(os.path.dirname(sys.executable), 'DLLs')
w = os.path.join(os.path.dirname(sys.executable), 'Lib')
e = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages')

q = []
for i in modules:
    ww = os.path.join(w, i)
    ee = os.path.join(e, i)
    if os.path.isdir(ww):
        a, b = ww, i
        q.append('--add-data "{}{}{}"'.format(a, os.pathsep, b))
        if i == 'sqlite3':
            dd1 = os.path.join(d, '_sqlite3.pyd')
            dd2 = os.path.join(d, 'sqlite3.dll')
            a, b = dd1, '.'
            q.append('--add-binary "{}{}{}"'.format(a, os.pathsep, b))
            a, b = dd2, '.'
            q.append('--add-binary "{}{}{}"'.format(a, os.pathsep, b))
    elif os.path.isdir(ee):
        a, b = ee, i
        q.append('--add-data "{}{}{}"'.format(a, os.pathsep, b))

v = ' '.join(q)
print(v)

# 上面的脚本根据你的 python 执行地址，大概会生成这样的内容 --add-data "D:\Python\Python36\Lib\site-packages\scrapy;scrapy" --add-data "D:\Python\Python36\Lib\email;email" --add-data "D:\Python\Python36\Lib\site-packages\twisted;twisted" --add-data "D:\Python\Python36\Lib\site-packages\queuelib;queuelib" --add-data "D:\Python\Python36\Lib\sqlite3;sqlite3" --add-binary "D:\Python\Python36\DLLs\_sqlite3.pyd;." --add-binary "D:\Python\Python36\DLLs\sqlite3.dll;."
# 使用时：在命令行输入 pyinstaller -F $你的脚本.py 并且将上面代码生成的内容抄下来拼接在后面就好了。
# 如果是单脚本可以考虑用下面的方式实现单脚本处理，并用上面的方式轻松打包代码
# 通常scrapy生成的大概会在 20M 左右，如果超过这个大小很多，可以去除 -F 生成代码包，看看多引入的哪些，然后增加 --exclude-module
# 例如 --exclude-module numpy --exclude-module scipy --exclude-module matplotlib
# 除非你需要这些库，否则上面这三个库随便一个都能成倍增长打包的文件的大小。
# scrapy 脚本编写以及中间件的插入使用请看下面的代码示例。




# scrapy 是一个项目，有很多文件夹怎么包在一起呢？
# 你需要使用单脚本来实现这个项目。所以脚本需要如下进行编写。
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import quote,unquote

class VSpider(scrapy.Spider):
    # 这里忽略，指代任意scrapy脚本代码
    ...

if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/bMXERwTjBD'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）
    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, cvs, xml, pickle, marshal
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
'''





# scrapy 有很多中间件怎么进行打包呢？
# 请详细看下面代码的处理方式，下面也展示了 scrapy 单脚本图片下载的处理方式，作为单脚本中间件加入的范例。
# 若有多余的引入库可能会导致打包成单个文件非常大，多检查。
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import quote,unquote

class VSpider(scrapy.Spider):
    # 这里忽略，指代任意scrapy脚本代码
    ...
    def parse(self, response):
        ...
        item = {}
        item['src'] = 'http://...' # 图片的真实路径
        yield item

if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/migSrTljNI'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, cvs, xml, pickle, marshal
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)

    # 动态中间件介绍
    # 通过实例动态增加中间件（解耦了之前只能通过配置中间件字符串），方便单脚本实现增加中间件功能，例如数据库存储方面的内容。
    # 便于单脚本利用别人的中间件。（将别人的中间件脚本粘贴进该脚本，实例化添加即可。示例如下，解开注释到 #(1) 即可测试。）
    # class VPipeline(object):
    #     def process_item(self, item, spider):
    #         print('\n==== 这里是动态增加的“下载中间件”部分 ====\n')
    #         return item
    # for i in p.crawlers: i.engine.scraper.itemproc._add_middleware(VPipeline()) #(1)
    # for i in p.crawlers: i.engine.scraper.spidermw._add_middleware(...)         #(2) 这里的...需要一个对应的中间件对象
    # for i in p.crawlers: i.engine.downloader.middleware._add_middleware(...)    #(3) 这里的...需要一个对应的中间件对象
    #1) 通过对象动态增加 itemmiddlewares，目前仅在数据管道部分这种处理方式比较常用（因默认item中间件为空，不会被默认配置影响）
    #2) 通过对象动态增加 spidermiddlewares     # i.engine.scraper.spidermw.middlewares        # 当前全部“爬虫中间件”
    #3) 通过对象动态增加 downloadermiddlewares # i.engine.downloader.middleware.middlewares   # 当前全部“下载中间件”
    #*) 注意: 2,3两种中间件的动态增加不常用。因 p.crawl 函数执行后就已初始化默认中间件。新的中间件只能“后添加”，缺乏灵活。
    #*）注意：1,2,3这三种中间件的添加方式只能在代码 p.crawl(VSpider) 与 p.start() 的中间，切记。

    # 图片下载中间件介绍
    # 图片相关的文件下载中间件的添加，注意：图片相关的资源需要绑定 spider 以及 crawler。示例如下。
    # 在一般的脚本 item['src'] 中添加字符串下载地址即可，一个 item 一个字符串下载地址，便于管理。不要按照默认方式添加下载列表
    import logging, hashlib
    from scrapy.pipelines.images import ImagesPipeline
    from scrapy.exceptions import DropItem
    class VImagePipeline(ImagesPipeline):
        def get_media_requests(self, item, info):
            yield Request(item['src']) 
        def file_path(self, request, response=None, info=None):
            url = request if not isinstance(request, Request) else request.url
            filename = hashlib.md5(url.encode()).hexdigest() # 或将存放的分类或名字通过 meta 传递，用 request.meta 获取
            return 'full/%s.jpg' % filename # 生成的图片文件名字，此处可增加多级分类路径（路径不存在则自动创建）
        def item_completed(self, results, item, info): # 判断下载是否成功
            k, v = results[0]
            if not k: logging.info('download fail {}'.format(item))
            else:     logging.info('download success {}'.format(item))
            item['image_download_stat'] = 'success' if k else 'fail'
            return item
    for i in p.crawlers: 
        vimage = VImagePipeline('./image') # 生成的文件地址，默认跟随脚本路径下生成的一个 image文件夹
        vimage.spiderinfo = vimage.SpiderInfo(i.spider)
        vimage.crawler = i
        i.engine.scraper.itemproc._add_middleware(vimage)

    p.start()
'''