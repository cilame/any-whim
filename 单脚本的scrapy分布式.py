# -*- coding: utf-8 -*-
def hook_to_scrapy_redis(namespace='default'):
    import redis
    from scrapy.http import Request
    from scrapy.utils.python import to_unicode, to_native_str
    from scrapy.utils.misc import load_object
    def request_to_dict(request, spider=None):
        if callable(request.callback): request.callback = _find_method(spider, request.callback)
        if callable(request.errback):  request.errback  = _find_method(spider, request.errback)
        d = {
            'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
            'callback': request.callback,
            'errback': request.errback,
            'method': request.method,
            'headers': dict(request.headers),
            'body': request.body,
            'cookies': request.cookies,
            'meta': request.meta,
            '_encoding': request._encoding,
            'priority': request.priority,
            'dont_filter': request.dont_filter,
            'flags': request.flags,
        }
        if type(request) is not Request:
            d['_class'] = request.__module__ + '.' + request.__class__.__name__
        return d
    def request_from_dict(d, spider=None):
        if d['callback'] and spider: d['callback'] = _get_method(spider, d['callback'])
        if d['errback']  and spider: d['errback']  = _get_method(spider, d['errback'])
        request_cls = load_object(d['_class']) if '_class' in d else Request
        _cls = request_cls(
            url=to_native_str(d['url']),
            callback=d['callback'],
            errback=d['errback'],
            method=d['method'],
            headers=d['headers'],
            body=d['body'],
            cookies=d['cookies'],
            meta=d['meta'],
            encoding=d['_encoding'],
            priority=d['priority'],
            dont_filter=d['dont_filter'],
            flags=d.get('flags'))
        return _cls
    def _find_method(obj, func):
        if obj: return func.__name__
        raise ValueError("Function %s is not a method of: %s" % (func, obj))
    def _get_method(obj, name):
        name = str(name)
        try:
            return getattr(obj, name)
        except AttributeError:
            raise ValueError("Method %r not found in: %s" % (name, obj))
    import pickle
    class _serializer:
        def loads(s):   return pickle.loads(s)
        def dumps(obj): return pickle.dumps(obj, protocol=-1)
    class BaseQueue(object):
        def __init__(self, server, spider, key):
            self.server = server
            self.spider = spider
            self.key = key % {'spider': spider.name}
            self.serializer = _serializer
        def _encode_request(self, request):         obj = request_to_dict(request, self.spider);  return self.serializer.dumps(obj)
        def _decode_request(self, encoded_request): obj = self.serializer.loads(encoded_request); return request_from_dict(obj, self.spider)
        def __len__(self):        raise NotImplementedError
        def push(self, request):  raise NotImplementedError
        def pop(self, timeout=0): raise NotImplementedError
        def clear(self):          self.server.delete(self.key)
    class FifoQueue(BaseQueue):
        def __len__(self):        return self.server.llen(self.key)
        def push(self, request):  self.server.lpush(self.key, self._encode_request(request))
        def pop(self, timeout=0):
            if timeout > 0:
                data = self.server.brpop(self.key, timeout)
                if isinstance(data, tuple):
                    data = data[1]
            else:
                data = self.server.rpop(self.key)
            if data:
                return self._decode_request(data)
    import logging
    from scrapy.dupefilters import BaseDupeFilter
    from scrapy.utils.request import request_fingerprint
    _logger = logging.getLogger(__name__)
    class RFPDupeFilter(BaseDupeFilter):
        logger = _logger
        def __init__(self, server, key, debug=False):
            self.server = server
            self.key = key
            self.debug = debug
            self.logdupes = True
        def request_seen(self, request): return self.server.sadd(self.key, self.request_fingerprint(request)) == 0
        def request_fingerprint(self, request): return request_fingerprint(request)
        def close(self, reason=''): self.clear()
        def clear(self): self.server.delete(self.key)
        def log(self, request, spider):
            if self.debug:
                msg = "Filtered duplicate request: %(request)s"
                self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            elif self.logdupes:
                msg = ("Filtered duplicate request %(request)s"
                       " - no more duplicates will be shown"
                       " (see DUPEFILTER_DEBUG to show all duplicates)")
                self.logger.debug(msg, {'request': request}, extra={'spider': spider})
                self.logdupes = False
    import pprint
    from datetime import datetime, timedelta
    class RedisStatsCollector:
        def __init__(self, crawler):
            self._spider_id_task_format = TASK_STATS
            self._dump      = crawler.settings.getbool('STATS_DUMP')
            self._local_max = 'DEPTH'
            self._maxdp     = 0
            self.server     = redis.StrictRedis(**REDIS_PARAMS)
            self.server.ping()
            self.encoding   = self.server.connection_pool.connection_kwargs.get('encoding')
        def get_stats(self, spider=None):
            _stat = {}
            for key,val in self.server.hgetall(self._spider_id_task_format).items():
                key,val = key.decode(self.encoding),val.decode(self.encoding)
                try:
                    if   key in ['finish_reason']:              _stat[key] = val
                    elif key in ['finish_time', 'start_time']:  _stat[key] = datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
                    else: _stat[key] = int(val) 
                except:
                    _stat[key] = val
            return _stat
        def set_value(self, key, value, spider=None):
            tname = self._spider_id_task_format
            if type(value) == datetime: value = str(value + timedelta(hours=8)) # 将默认utc时区转到中国，方便我使用
            self.server.hsetnx(tname, key, value)
        def inc_value(self, key, count=1, start=0, spider=None):
            if spider: self.server.hincrby(self._spider_id_task_format, key, count)
        def max_value(self, key, value, spider=None):
            if value > self._maxdp: self._maxdp = value; self.server.hset(self._spider_id_task_format, key, value)
        def open_spider(self, spider): pass
        def close_spider(self, spider, reason):
            if self._dump:
                _logger.info("Dumping Scrapy stats:\n" + pprint.pformat(self.get_stats(spider)), extra={'spider': spider})
    class Scheduler(object):
        def __init__(self, server, persist=False, flush_on_start=False, idle_before_close=0):
            self.server = server
            self.persist = persist
            self.flush_on_start = flush_on_start
            self.idle_before_close = idle_before_close
            self.stats = None
            self.queue_key = QUEUE_KEY
            self.dupefilter_key = DUPEFILTER_KEY
        def __len__(self): return len(self.queue)
        @classmethod
        def from_settings(cls, settings):
            server = redis.StrictRedis(**REDIS_PARAMS)
            server.ping()
            return cls(server=server, **EXTRA_SETTING)
        @classmethod
        def from_crawler(cls, crawler):
            instance = cls.from_settings(crawler.settings)
            instance.stats = crawler.stats
            return instance
        def open(self, spider):
            self.spider = spider
            try: self.queue = FifoQueue(server=self.server, spider=spider, key=self.queue_key % {'spider': spider.name})
            except TypeError as e: raise ValueError("Failed to instantiate queue class '%s': %s", self.queue_cls, e)
            try: self.df = RFPDupeFilter(server=self.server, key=self.dupefilter_key % {'spider': spider.name}, debug=False)
            except TypeError as e: raise ValueError("Failed to instantiate dupefilter class '%s': %s", self.dupefilter_cls, e)
            if self.flush_on_start: self.flush()
            if len(self.queue): spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))
        def close(self, reason): 
            if not self.persist: self.flush()
        def flush(self): self.df.clear(); self.queue.clear()
        def enqueue_request(self, request):
            if not request.dont_filter and self.df.request_seen(request): self.df.log(request, self.spider); return False
            if self.stats: self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
            self.queue.push(request)
            return True
        def next_request(self):
            block_pop_timeout = self.idle_before_close
            request = self.queue.pop(block_pop_timeout)
            if request and self.stats: self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
            return request
        def has_pending_requests(self): return len(self) > 0
    from scrapy import signals
    from scrapy.core.scraper import Scraper
    from scrapy.core.engine import ExecutionEngine
    from scrapy.utils.misc import load_object
    def __hook_init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self.settings = crawler.settings
        self.signals = crawler.signals
        self.logformatter = crawler.logformatter
        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls = Scheduler
        downloader_cls = load_object(self.settings['DOWNLOADER'])
        self.downloader = downloader_cls(crawler)
        self.scraper = Scraper(crawler)
        self._spider_closed_callback = spider_closed_callback
    ExecutionEngine.__init__ = __hook_init__
    _bak_next_request = ExecutionEngine._next_request
    START_TOGGLE_HOOK = True
    def __hook_next_request(self, spider):
        nonlocal START_TOGGLE_HOOK
        if START_TOGGLE_HOOK:
            r = self.crawler.stats.server.hincrby(TASK_STATS, 'start_toggle_requests')
            if r != 1: self.slot.start_requests = None # 让其他非首次启动的 start_requests 不执行
            START_TOGGLE_HOOK = False
        _bak_next_request(self, spider)
    ExecutionEngine._next_request = __hook_next_request
    import scrapy.spiders
    from scrapy import signals
    from scrapy.exceptions import DontCloseSpider
    from scrapy.spiders import Spider
    class RedisMixin(object):
        redis_key = None
        redis_batch_size = None
        redis_encoding = None
        server = None
        def start_requests(self): return self.next_requests()
        def setup_redis(self, crawler=None):
            if self.server is not None: return
            settings = crawler.settings
            self.redis_key = QUEUE_KEY
            self.redis_batch_size = settings.getint('CONCURRENT_REQUESTS')
            self.server = redis.StrictRedis(**REDIS_PARAMS)
            crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        def next_requests(self):
            fetch_one = self.server.lpop
            found = 0
            while found < self.redis_batch_size:
                data = fetch_one(self.redis_key)
                if not data: break
                req = self.make_request_from_data(data)
                if req:
                    yield req
                    found += 1
                else:
                    self.logger.debug("Request not made from data: %r", data)
            if found:
                self.logger.debug("Read %s requests from '%s'", found, self.redis_key)
        def make_request_from_data(self, data): return self.make_requests_from_url(data.decode(self.redis_encoding))
        def schedule_next_requests(self):
            for req in self.next_requests(): self.crawler.engine.crawl(req, spider=self)
        def spider_idle(self):
            self.schedule_next_requests()
            raise DontCloseSpider
    class RedisSpider(RedisMixin, Spider):
        @classmethod
        def from_crawler(self, crawler, *args, **kwargs):
            obj = super(RedisSpider, self).from_crawler(crawler, *args, **kwargs)
            obj.setup_redis(crawler)
            return obj
    scrapy.Spider = RedisSpider
    import scrapy.spiders
    import scrapy.extensions.telnet
    import scrapy.extensions.memusage
    import scrapy.extensions.logstats
    import scrapy.statscollectors
    scrapy.extensions.telnet.TelnetConsole.__init__  = lambda self,_:None   # 关闭这个插件，我不用(这种关闭插件的方式小孩子可不要学哦~)
    scrapy.extensions.memusage.MemoryUsage.__init__  = lambda self,_:None   # 同样的理由，我不用
    scrapy.extensions.logstats.LogStats.from_crawler = lambda self:None     # 同样的理由，我不用
    scrapy.statscollectors.MemoryStatsCollector = RedisStatsCollector       # 挂钩默认日志，让其自动支持redis日志(这种抽象的钩子技术小孩子可不要学哦~)
    import json
    import scrapy.pipelines
    from scrapy.core.spidermw import SpiderMiddlewareManager
    TASK_COLLECTION = None
    class VRedisPipeline(object):
        def __init__(self):
            self.key = TASK_COLLECTION
            self.server = redis.StrictRedis(**REDIS_PARAMS)
            self.server.ping()
        def process_item(self, item, spider):
            if self.key:
                self.server.lpush(self.key, json.dumps(item))
            return item
    def __hook_scraper_init__(self, crawler):
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        itemproc_cls = scrapy.pipelines.ItemPipelineManager()
        self.itemproc = itemproc_cls.from_crawler(crawler)
        self.itemproc._add_middleware(VRedisPipeline()) # 挂钩scraper的初始化，在此刻增加redis写入中间件
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler
        self.signals = crawler.signals
        self.logformatter = crawler.logformatter
    import scrapy.core.scraper
    scrapy.core.scraper.Scraper.__init__ = __hook_scraper_init__
    EXTRA_SETTING = {
        'persist': True,            # 任务(意外或正常)结束是否保留过滤池或任务队列
        'flush_on_start': False,    # 任务开始时是否需要进行队列和过滤池的清空处理(测试时使用)
        'idle_before_close': 0,     # 约等于redis中的(包括且不限于)函数 brpop(key,timeout) 中的参数 timeout
    }
    REDIS_PARAMS = {
        'host':'127.0.0.1',
        'port':6379,
        'password': None,
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
        'retry_on_timeout': True,
        'encoding': 'utf-8',
    }
    QUEUE_KEY       = 'scrapy_redis:{}:TASK_QUEUE'.format(namespace)  # 任务队列(当任务正常执行完，必然是空)
    DUPEFILTER_KEY  = 'scrapy_redis:{}:DUPEFILTER'.format(namespace)  # 过滤池(用于放置每个请求的指纹)
    TASK_STATS      = 'scrapy_redis:{}:TASK_STATS'.format(namespace)  # 任务状态日志
    TASK_COLLECTION = 'scrapy_redis:{}:COLLECTION'.format(namespace)  # 数据收集的地方(默认使用redis收集json.dumps的数据)，注释这行数据就不收集到redis

hook_to_scrapy_redis(namespace='vilame') # 用函数将各类钩子处理包住，防止污染全局变量










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
        'COOKIES_ENABLED': False,  # use my create cookie in headers
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://baidu.com'
            )
            url = quote_val(url)
            headers = {}
            return url,headers

        for i in range(1):
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
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.
        for i in range(5):
            # if i == 4:
            #     raise 123
            d = {}
            d['1231231'] = 1111
            d['3333333'] = 1111
            yield d

        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.baidu.com/s?ie=UTF-8&wd=123'
            )
            url = quote_val(url)
            headers = {}
            return url,headers

        for i in range(3):
            url,headers = mk_url_headers()
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_info,
                    meta     = meta,
                )
            yield r

    def parse_info(self, response):
        for i in range(2):
            d = {}
            d['2222222'] = 1111
            d['33334444444333'] = 1111
            yield d

        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.baidu.com/s?ie=UTF-8&wd=1233'
            )
            url = quote_val(url)
            headers = {}
            return url,headers

        for i in range(3):
            url,headers = mk_url_headers()
            meta = {}
            meta['proxy'] = self.proxy
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_info_info,
                    meta     = meta,
                )
            yield r

    def parse_info_info(self, response):
        yield {"你好":"i兄弟"}

# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/vyBAlfzQSt'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        # 'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
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
