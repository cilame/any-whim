# 如果出现编码异常，可以尝试解开下面注释中的代码以处理 execjs 执行时期的编码问题。
import subprocess
_bak_Popen = subprocess.Popen
def _Popen(*a, **kw):
    kw['encoding'] = 'utf-8'
    return _bak_Popen(*a, **kw)
subprocess.Popen = _Popen

import execjs
with open('./携程.js',encoding='utf-8') as f:
    jsenv = f.read()

def make_fun():
    ctx = execjs.compile(jsenv)
    def get_id(jscode):
        return ctx.call('test', jscode)
    return get_id






import json

import requests
from lxml import etree

def post_info():
    def mk_url_headers_body():
        url = (
            'https://m.ctrip.com/restapi/soa2/21881/getHotelScript'
        )
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        body = {
            "callback": "MqzHdwmKRm",
            "a": 0,
            "b": "2021-07-25",
            "c": "2021-07-26",
            "d": "zh-cn",
            "e": 2,
            "webpSupport": True,
            "platform": "online",
            "pageID": "102002",
            "head": {
                "Version": "",
                "userRegion": "CN",
                "Locale": "zh-CN",
                "LocaleController": "zh-CN",
                "TimeZone": "8",
                "Currency": "CNY",
                "PageId": "102002",
                "webpSupport": True,
                "userIP": "",
                "P": "18646827243",
                "ticket": "",
                "clientID": "1626676085429.lkwzm",
                "group": "ctrip",
                "Frontend": {
                    "vid": "1626676085429.lkwzm",
                    "sessionID": 5,
                    "pvid": 36
                },
                "Union": {
                    "ouid": "dt001",
                    "AllianceID": "4897",
                    "SID": "799749",
                    "Ouid": "dt001"
                },
                "HotelExtension": {
                    "group": "CTRIP",
                    "hasAidInUrl": False,
                    "Qid": "670483988263",
                    "WebpSupport": True
                }
            }
        }
        body = json.dumps(body, separators=(',', ':'))
        return url,headers,body

    url,headers,body = mk_url_headers_body()
    s = requests.post(url,headers=headers,data=body) 
    jsondata = s.json()
    jscode = '((window=self=this).Window=()=>"native code",this).Image=class{};MqzHdwmKRm=e=>MqzHdwmKRm=e;'+jsondata['Response']+';MqzHdwmKRm()'

    get_id = make_fun()
    v = get_id(jscode)
    print(v)



post_info()

#
