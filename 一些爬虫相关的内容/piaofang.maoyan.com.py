#coding=utf-8
import os
import re
import json
import hashlib
import requests

def get_info():
    def mk_url_headers():
        url = (
            'http://piaofang.maoyan.com/dashboard-ajax'
            '?orderType=0'
            '&uuid=176dbd8ace1c8-0423b147cc35ae-5c19341b-140000-176dbd8ace2c8'
            '&riskLevel=71'
            '&optimusCode=10'
        )
        headers = {
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    jsondata = json.loads(s.text)
    def get_number_func(url):
        # 这个网页（猫眼实时票房榜）的字体加密比较简单，字体文件很小，且固定只有五种所以处理起来比较简单
        bitfile  = requests.get(fonturl).content
        _numbermap = {
            '2c97a0c666450eba2bdbd9a75babd9c6': {
                '&#xE20B': 6, '&#xE52E': 9, '&#xE644': 2, '&#xE8CD': 7, '&#xE93F': 0,
                '&#xED63': 8, '&#xEE55': 4, '&#xF00D': 3, '&#xF364': 1, '&#xF438': 5, },
            '098f23bc1eec5d16622b9a279e08b31c': {
                '&#xE208': 5, '&#xE64F': 2, '&#xEC32': 9, '&#xECC6': 6, '&#xEDAA': 7,
                '&#xEF48': 1, '&#xF0E9': 3, '&#xF41F': 4, '&#xF7F8': 0, '&#xF823': 8, },
            '0846a06bc1b7f8f8aa9ed426b11f34ed': {
                '&#xE1A8': 2, '&#xE26E': 7, '&#xE285': 5, '&#xE520': 6, '&#xE8C2': 8,
                '&#xEF66': 9, '&#xF0AA': 4, '&#xF0D3': 1, '&#xF0EE': 3, '&#xF590': 0, },
            '3076b941fb19107f1bcf0e030061835e': {
                '&#xE0F3': 9, '&#xE260': 8, '&#xE349': 5, '&#xE5C6': 0, '&#xE5D0': 7,
                '&#xE6F5': 6, '&#xECA5': 1, '&#xED51': 4, '&#xF603': 3, '&#xF771': 2, },
            'deee16b549af29e7fd49f97300e84a13': {
                '&#xE2C0': 3, '&#xE3F3': 6, '&#xE6E5': 5, '&#xE75C': 7, '&#xEB99': 1,
                '&#xF119': 4, '&#xF1D2': 8, '&#xF1E8': 0, '&#xF4D0': 9, '&#xF5A3': 2, },
        }
        numbmap = _numbermap[hashlib.md5(bitfile).hexdigest()]
        return lambda dic:float(re.sub('&#x(.{4});', lambda e:str(numbmap['&#x' + e.group(1).upper()]), dic))
    fonturl = 'http:'+re.findall(r'"([^"]+\.woff)"', jsondata['fontStyle'])[0]
    get_number = get_number_func(fonturl)
    for i in jsondata['movieList']['data']['list']:
        d = {}
        d["avgShowView"]              = i.get("avgShowView")       # 2
        d["showCount"]                = i.get("showCount")         # 362
        d["avgSeatView"]              = i.get("avgSeatView")       # 1.2%
        d["showCountRate"]            = i.get("showCountRate")     # 0.1%
        d["boxRate"]                  = i.get("boxRate")           # <0.1%
        d["splitBoxRate"]             = i.get("splitBoxRate")      # <0.1%
        d["sumSplitBoxDesc"]          = i.get("sumSplitBoxDesc")   # 159.0万
        d["sumBoxDesc"]               = i.get("sumBoxDesc")        # 167.7万
        d["boxSplitUnit"]             = i.get("boxSplitUnit")      # {'num': '&#xeb99;.&#xeb99;&#xe6e5;', 'unit': '万'}
        d["splitBoxSplitUnit"]        = i.get("splitBoxSplitUnit") # {'num': '&#xeb99;.&#xf1e8;&#xf4d0;', 'unit': '万'}
        d["movieInfo"]                = i.get("movieInfo")         # {'movieId': 1353263, 'movieName': '小破孩大状元', 'releaseInfo': '
        d["boxSplitUnit"]['num']      = get_number(d["boxSplitUnit"]['num'])
        d["splitBoxSplitUnit"]['num'] = get_number(d["splitBoxSplitUnit"]['num'])
                                                            # 上映8天'}
        print('------------------------------ split ------------------------------')
        import pprint
        pprint.pprint(d)

get_info()

#
