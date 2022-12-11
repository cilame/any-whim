# encoding=utf-8

import re
import requests
from lxml import etree

def get_simple_path_tail(e):
    root = e.getroottree()
    try:
        xp = root.getelementpath(e)
    except:
        return
    v = xp.count('/')
    # 优先找路径上的id和class项优化路径
    for i in range(v):
        xpa = xp.rsplit('/',i)[0]
        rke = '/'.join(xp.rsplit('/',i)[1:])
        ele = root.xpath(xpa)[0].attrib
        tag = root.xpath(xpa)[0].tag
        if 'id' in ele:
            key = '[@id="{}"]'.format(ele["id"])
            rke = '/'+rke if rke else ""
            val = '//{}{}{}'.format(xpa.rsplit('/',1)[1],key,rke)
            return xp,val,key
        if 'class' in ele:
            if ' ' in ele["class"] and not ele["class"].startswith(' '):
                elass = ele["class"].split(' ',1)[0]
            else:
                elass = ele["class"]
            key = '[@class="{}"]'.format(elass)
            rke = '/'+rke if rke else ""
            val = '//{}{}{}'.format(xpa.rsplit('/',1)[1],key,rke)
            if not elass.strip():
                continue
            return xp,val,key


# 对列表的优化处理
def get_simple_path_head(p,lilimit=5):
    # 先通过绝对xpath路径进行分块处理
    s = {}
    w = {}
    for xp, sxp, key in p:
        q = re.sub('\[\d+\]','',xp)#.rsplit('/',1)[0]
        if q not in s:
            s[q] = [[xp, sxp, key]]
        else:
            s[q].append([xp, sxp, key])
    rm = []
    for px in sorted(s,key=lambda i: -len(i)):
        xps,sxps,keys = zip(*s[px])
        if len(sxps) == len(set(sxps)): continue
        p = {}
        ls = list(set(keys))
        for j in s[px]:
            if j[2] not in p:
                p[j[2]] = [j]
            else:
                p[j[2]].append(j)
        for i in p:
            le = len(p[i])
            v = ''
            if le > lilimit:
                for idx in range(p[i][0][0].count('/')):
                    v = p[i][0][0].rsplit('/',idx)[0]
                    q = list(map(lambda i:i[0].startswith(v),p[i]))
                    if all(q):
                        break
                for idx,j in enumerate(p[i]):
                    a,b,c = j
                    t = '/{}{}'.format(a.replace(v,''),c) + b.split(c,1)[1]
                    t = t if t.startswith('//') else '/' + t
                    p[i][idx][1] = t
                    p[i][idx].append(px)
                    yield j

def get_xpath_by_str(strs, html_content):
    e = etree.HTML(html_content)
    q = []
    p = []
    for i in e.xpath('//*'):
        xps = get_simple_path_tail(i) 
        if xps:
            xp, sxp, key = xps
            if sxp not in q:
                q.append(xp)
                p.append([xp, sxp, key])
    p.sort(key=lambda i: -len(i[0]))
    p = get_simple_path_head(p)
    for key, xp, sxp, px in p:
        v = e.xpath('string({})'.format(xp))
        if strs in v:
            yield xp,v

url = (
    'http://china.findlaw.cn/ask/browse_t00_page2/'
)

url = 'https://search.jd.com/Search?keyword=123'

headers = {
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}

def get(url,headers):
    s = requests.get(url,headers=headers)
    e = etree.HTML(s.content)
    return e,s.content

e,content = get(url,headers)
for i in get_xpath_by_str('123',content):
    print(i)
