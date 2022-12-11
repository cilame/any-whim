# 如果出现编码异常，可以尝试解开下面注释中的代码以处理 execjs 执行时期的编码问题。
import subprocess
_bak_Popen = subprocess.Popen
def _Popen(*a, **kw):
    kw['encoding'] = 'utf-8'
    return _bak_Popen(*a, **kw)
subprocess.Popen = _Popen

import execjs
def make_func(code):
    with open('./boss.js', encoding='utf-8') as f:
        jstitle = f.read()
    jscode = jstitle + code + '''
    ;function test(seed, time) {
        code = encodeURIComponent((new window.ABC).z(seed, parseInt(time) + (480 + (new Date).getTimezoneOffset()) * 60 * 1e3));
        return "__zp_stoken__=" +code;
    }; 
    '''
    ctx = execjs.compile(jscode)
    def get__zp_stoken__(seed, time):
        return ctx.call('test', seed, time)
    return get__zp_stoken__

# {o}h40SEN4dX^DjW678zzTXo(G09AZm9MpQiKP<3aDJiqcs~PA!8b~_?Mhu-s-gn7PfHBW`Ze@dY9)ZgG$WpZuYHcY#6lgeTI19;QExXs;51%uo{6JxnB(oxP)Zbq<n2wK_|tb26~fO(TYSvi#S>Qu2bcNbCer4-$JN$^KWD<CN`tds!vYW+Qu)wIR&d)M;1TV?E8BA=sbs|jYWcm!`15{WB*e7TIqgx#87gelU*nRx!wbf1K9jzFy}Us9rpX^E;ftEI(zJl|FTA>;%Z<6qp5)qNx@f0b<fx#$(DLwe#0%`Z866~=|0c`>5wYSfSLivg##qicV;=Vb1<*RBgoIL!F13)^;4dT^p{E{j2ixX^CFg?<5!1R$%g@b>5^rJ{CAFm4*bqAa6)s&cVOTuA

import re
from urllib.parse import unquote, quote
import requests

def get_info():
    def mk_url_headers():
        url = 'https://www.zhipin.com/gongsi/?page=2&ka=page-2'
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers

    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers,allow_redirects=False)
    location = s.headers['location']
    seed = unquote(re.findall('seed=([^&]+)&', location)[0])
    name = unquote(re.findall('name=([^&]+)&', location)[0])
    ts = unquote(re.findall('ts=([^&]+)&', location)[0])

    def mk_url_headers(name):
        url = 'https://www.zhipin.com/web/common/security-js/{}.js'.format(name)
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    # 此处可以不必每次都要请求，这里搞个缓存即可。
    url,headers = mk_url_headers(name)
    s = requests.get(url,headers=headers)
    code = s.text

    get__zp_stoken__ = make_func(code)
    __zp_stoken__ = get__zp_stoken__(seed, ts)

    def mk_url_headers():
        url = 'https://www.zhipin.com/gongsi/?page=2&ka=page-2'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": (
                __zp_stoken__
            ),
            "Host": "www.zhipin.com",
            "Pragma": "no-cache",
            "Referer": "https://www.zhipin.com/web/common/security-check.html?seed=5zWxaCvz%2Ba%2BDdQboYYGBpAypxywNUfCMms9dmdLF%2BNg%3D&name=84e96a33&ts=1626876786296&callbackUrl=%2Fgongsi%2F%3Fpage%3D2%26ka%3Dpage-2&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fgongsi%2F%3Fka%3Dheader_brand",
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    print('BOSS直聘' in s.text, __zp_stoken__)

for i in range(10):
    get_info()