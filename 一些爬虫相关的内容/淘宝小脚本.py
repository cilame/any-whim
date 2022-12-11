import requests
from lxml import etree
import re
import json

def get_html_content(url,have_cookie=True):
    if have_cookie:
        # 如果出现错误，可能是因为翻页的接口使用太频繁。
        # 用浏览器手动过一下验证，然后从 F12里面新的cookie的部分重新粘一次进来就好了。
        headers = '''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9
        cache-control: max-age=0
        cookie: t=235454bdf1cb0fbbe861ac3706988afe; cna=d+R/FDkF+QUCASQYJDzifXR8; thw=cn; tracknick=jiarang_2304; tg=0; enc=nw68QCvglRyKtJnuLV6V8jxZitU9gWgVBPYR9A1YHt1eQPFjYcEi5rVtNOL4cnLqf8wFJuPpHy9YCMrYoWnzJw%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; _cc_=URm48syIZQ%3D%3D; miid=1079373766217317383; mt=ci%3D-1_1; cookie2=15bf348a98cf3151f9f46ac32a11a24b; v=0; _tb_token_=3d3e19eb7a87; _uab_collina=154695129431962686737663; x5sec=7b227365617263686170703b32223a223138353138366363646262643264383835316236393030383065316238383735434b374430754546454c2f4439722f41726553672f514561444449794d5451344e6a63794e544d374d513d3d227d; JSESSIONID=DF56D903F4B026A63DB860139E0856B4; l=aBv8yAcKybDfANBXtMa2VXTWB7076CBPeLnY1MaHVTEhNPV17RXy1jno-VwWj_qC5Jcy_K-5F; isg=BObmTL0DhkWNzFUt9oYujkoGN1yobyjl9O67ctCP0onkU4ZtOFd6kcwhrw_6eyKZ
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
        '''
    else:
        headers = '''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
        '''
    headers = {i.split(':',1)[0].strip():i.split(':',1)[1].strip() for i in headers.splitlines() if i.strip()}
    s = requests.get(url,headers=headers)
    return s.text


def parse_content(content):
    def parse_model(q):
        # 你自己把这里需要的字段自己填充完整
        # dict对象的get方法如果get不到是直接返回None的
        # 这样的话参数列表里面的值就是None不用自己再一个个 if else 了
        # 这里很可能收集不要完全，这要要多注意一下。
        d = {}
        d["__TITLE__"] = q.get("__TITLE__")
        d["__PRICE__"] = q.get("__PRICE__")
        d["生产许可证编号"] = q.get("生产许可证编号")
        d["产品标准号"] = q.get("产品标准号")
        d["厂名"] = q.get("厂名")
        d["厂址"] = q.get("厂址")
        d["厂家联系方式"] = q.get("厂家联系方式")
        d["配料表"] = q.get("配料表")
        d["储藏方法"] = q.get("储藏方法")
        d["保质期"] = q.get("保质期")
        d["食品添加剂"] = q.get("食品添加剂")
        d["净含量"] = q.get("净含量")
        d["包装方式"] = q.get("包装方式")
        d["品牌"] = q.get("品牌")
        d["系列"] = q.get("系列")
        d["商品条形码"] = q.get("商品条形码")
        d["肉类产品"] = q.get("肉类产品")
        d["食品工艺"] = q.get("食品工艺")
        d["是否含糖"] = q.get("是否含糖")
        d["产地"] = q.get("产地")
        d["省份"] = q.get("省份")
        d["城市"] = q.get("城市")
        return d

    e = etree.HTML(content)
    q = []
    if 'tmall' in url:
        # 天猫的解析
        info = e.xpath('string(//script[contains(text(),"TShop.poc")])')
        info = json.loads(info.split('TShop.Setup(',1)[1].rsplit('"}',1)[0]+'"}')
        name, price = info['itemDO']['title'], info['detail']['defaultItemPrice']
        q.append(['__TITLE__',name])
        q.append(['__PRICE__',price])
        for i in e.xpath('//ul[@id="J_AttrUL"]/li'):
            v = i.xpath('./text()')[0].replace('\xa0','')
            v = list(map(lambda i:i.strip(),re.split('[：:]',v,1)))
            q.append(v)
    else:
        # 淘宝的解析
        price = e.xpath('//input[@name="current_price"]/@value')[0]
        name = e.xpath('//h3[@class="tb-main-title"]/@data-title')[0]
        q.append(['__TITLE__',name])
        q.append(['__PRICE__',price])
        for i in e.xpath('//ul[contains(@class,"attributes-list")]/li'):
            v = i.xpath('./text()')[0].replace('\xa0','')
            v = list(map(lambda i:i.strip(),re.split('[：:]',v,1)))
            q.append(v)
    return parse_model(dict(q))


def parse_urls(content):
    # 这里是解析翻页的部分。注意一下，这里的翻页是需要用到 cookie验证的。
    # 并且这个接口使用太快会出现验证窗口，到时候就需要重新在代码里写入 headers
    e = etree.HTML(content)
    info = e.xpath('string(//script[contains(text(),"g_page_config")])')
    info = json.loads(('{' + info.split('{',1)[1]).rsplit('g_srp_loadCss();',1)[0].strip()[:-1])
    for i in info['mods']['itemlist']['data']['auctions']:
        if i['comment_url'].startswith('//item.taobao.com/'):
            yield 'https://item.taobao.com/item.htm?id={}'.format(i['nid'])
        elif i['comment_url'].startswith('//detail.tmall.com/'):
            yield 'https://detail.tmall.com/item.htm?id={}'.format(i['nid'])
        else:
            continue


key = '食品'
list_url_model = 'https://s.taobao.com/search?q={}&s={}'
toggle = False
start_page = 1

for i in range(100):
    page = i+1
    if page >= start_page: # 从第几页开始
        toggle = True
    if toggle:
        print('page:{}.'.format(page))
        list_url = list_url_model.format(key, i*44)
        ucontent = get_html_content(list_url)
        for url in parse_urls(ucontent):
            print('========================')
            print(url)
            content = get_html_content(url,have_cookie=False)# 商品页面不需要cookie验证。
            data = parse_content(content)
            import pprint
            pprint.pprint(data)

