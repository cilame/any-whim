# -*- coding:utf-8 -*- 
import requests
import re
from lxml import etree

def normal_content(content,
                   tags=['script','style','select','noscript'],
                   rootxpath='//html'):
    # 通用文本提取函数
    if type(content) is bytes:
        try:
            c = content.decode('utf-8')
        except:
            c = content.decode('gbk')
    elif type(content) is str:
        c = content
    else:
        raise 'content type must in [bytes, str].'
    # 针对部分网页汉字粘连的问题的处理，增强鲁棒性。
    c = re.sub('>([^>]*[\u4e00-\u9fa5]{1,}[^<]*)<','>\g<1> <',c)
    e = etree.HTML(c)
    q = []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    t = e.xpath('normalize-space({})'.format(rootxpath))
    return t.strip()

url = 'http://www.pingan.com/official/insurance?secondclass=4617947d7ded73bd&flag=47b8b71a21e9494e'
s = requests.get(url)
t = normal_content(s.content)
print(t)
