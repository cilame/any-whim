#coding=utf-8

import os
import re
import json
import base64
import shutil
import tempfile

import requests
from lxml import etree
from fontTools.ttLib import TTFont

def get_info(page):
    def mk_url_headers(page):
        url = (
            'http://match.yuanrenxue.com/api/match/7'
            '?page={}'
        ).format(page)
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "yuanrenxue.project"
        }
        return url,headers

    url,headers = mk_url_headers(page)
    s = requests.get(url,headers=headers)
    jsondata = json.loads(s.text)
    bitfile  = base64.b64decode(jsondata['woff'].encode())
    temppath = None
    try:
        temppath = tempfile.mkdtemp()
        filename = os.path.join(temppath, 'woff.ttf')
        filexml  = os.path.join(temppath, 'woff.xml')
        with open(filename, 'wb') as f:
            f.write(bitfile)
        font = TTFont(filename)
        font.saveXML(filexml)
        with open(filexml) as f:
            xmlstring = f.read()
    finally:
        if temppath and os.path.isdir(temppath): 
            shutil.rmtree(temppath)
    finger = {
        (13, 13)     : 0,
        (10,)        : 1,
        (30,)        : 2,
        (44,)        : 3,
        (11, 4)      : 4,
        (37,)        : 5,
        (28, 13)     : 6,
        (7,)         : 7,
        (32, 13, 12) : 8,
        (29, 12)     : 9,
    }
    xmlstring = xmlstring.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    e = etree.HTML(xmlstring)
    number_map = {}
    for i in e.xpath('//ttglyph[contains(@name, "uni")]'):
        number = finger[tuple([len(j.xpath('./pt')) for j in i.xpath('./contour')])]
        name = i.xpath('./@name')[0].replace('uni', '&#x')
        number_map[name] = number
    def get_number(fontstr):
        return int(''.join([str(number_map[i]) for i in fontstr.strip().split()]))
    page_numbers = [get_number(i['value']) for i in jsondata['data']]
    return page_numbers

allvalues = []
for page in range(1, 6):
    values = get_info(page)
    print('page:{} --> values:{}'.format(page, values))
    allvalues.extend(values)


names = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖', '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀', '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮', '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子', '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚', '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']
vmaps = dict(zip(allvalues, names[1:len(allvalues)]))
print(vmaps)
print('max:{} name:{}'.format(max(vmaps), vmaps[max(vmaps)]))

# 正常输出结果
# page:1 --> values:[3236, 5041, 3958, 8550, 7037, 8898, 2190, 8400, 4500, 7478]
# page:2 --> values:[2342, 1926, 5826, 2827, 369, 4384, 2934, 5468, 9107, 2132]
# page:3 --> values:[5553, 687, 5688, 6179, 7722, 35, 6301, 9221, 6534, 9711]
# page:4 --> values:[6995, 3705, 5413, 2333, 5660, 7142, 8826, 9291, 5778, 2920]
# page:5 --> values:[5983, 9015, 1533, 4337, 746, 4349, 4229, 4928, 2830, 1206]
# {3236: '爷灬霸气傀儡', 5041: '梦战苍穹', 3958: '傲世哥', 8550: 'мaη肆風聲', 7037: '一刀メ隔世', 8898: '横刀メ绝杀', 2190: 'Q不死你R死你', 8400: '魔帝殤邪', 4500: '封刀不再战', 7478: '倾城孤狼', 2342: '戎马江湖', 1926: '狂得像风', 5826: '影之哀伤', 2827: '謸氕づ独尊', 369: '傲视狂杀', 4384: '追风之梦', 2934: '枭雄在世', 5468: '傲视之巅', 9107: '黑夜刺客', 2132: '占你心为王', 5553: '爷来取你狗命', 687: '御风踏血', 5688: '凫矢暮城', 6179: '孤影メ残刀', 7722: '野区霸王', 35: '噬血啸月', 6301: '风逝无迹', 9221: '帅的睡不着', 6534: '血色杀戮者', 9711: '冷视天下', 6995: '帅出新高度', 3705: '風狆瑬蒗', 5413: '灵魂禁锢', 2333: 'ヤ地狱篮枫ゞ', 5660: '溅血メ破天', 7142: '剑尊メ杀戮', 8826: '塞外う飛龍', 9291: '哥‘K纯帅', 5778: '逆風祈雨', 2920: '恣意踏江山', 5983: '望断、天涯路', 9015: '地獄惡灵', 1533: '疯狂メ孽杀', 4337: '寂月灭影', 746: '骚年霸称帝王', 4349: '狂杀メ无赦', 4229: '死灵的哀伤', 4928: '撩妹界扛把子', 2830: '霸刀☆藐视天下'}
# max:9711 name:冷视天下