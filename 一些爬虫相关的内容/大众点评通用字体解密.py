# 直接执行代码即可测试
# python3

import re
import requests

def get_font_dict(url):
    def mk_font_dict(url):
        def mk_url_headers(url):
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(url)
        s = requests.get(url,headers=headers,verify=False)
        font_size = 14
        start_y = 23
        font_dict = {}
        y_list = re.findall(r'd="M0 (\d+?) ', s.content.decode())
        if y_list:
            font_list = re.findall(r'textPath .*?>(.*?)<', s.content.decode())
            for i, string in enumerate(font_list):
                y_offset = start_y - int(y_list[i])
                for j, font in enumerate(string):
                    x_offset = -j * font_size
                    font_dict[(x_offset, y_offset)] = font
        else:
            font_list = re.findall(r'<text x="0" y="(.*?)">(.*?)</text>', s.content.decode())
            for y, string in font_list:
                y_offset = start_y - int(y)
                for j, font in enumerate(string):
                    x_offset = -j * font_size
                    font_dict[(x_offset, y_offset)] = font
        return font_dict
    return mk_font_dict(url)

def get_css_font_dict(url):
    def mk_css_font_dict(url):
        def mk_url_headers(url):
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(url)
        s = requests.get(url,headers=headers,verify=False)
        content = s.content.decode()
        svgs = re.findall(r'url\((//s3plus.sankuai.com/[^\)]+\.svg)\)', content)
        font_dict = get_font_dict('http:' + svgs[0]) # 通常这里的第一个就是需要的字体数据的 url 链接。
        css_dict = {}
        _exp1 = r'\.(.{5}){background:(.*?).0px (.*?).0px;}'
        _exp2 = r'\.(.{6}){background:(.*?).0px (.*?).0px;}'
        css_items = re.findall(_exp1, content, flags=re.S) or re.findall(_exp2, content, flags=re.S)
        for a,b,c in css_items:
            css_dict[a] = (int(b), int(c))
        return css_dict, font_dict
    return mk_css_font_dict(url)

def get_html_content():
    # 请配置头信息中的的 cookie 内容让正常的加密 HTML 文本结果返回，后再进行解密！！！！！！！！！
    def mk_url_headers():
        url = 'http://www.dianping.com/shop/9972787/review_all/p1'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": (
                "_hc.v=e2010187-0fb3-aa0b-664c-f654e53338c2.1574739490; "
                "_lxsdk=16ea5c9b2f0c8-08cd26d4feb846-2393f61-1fa400-16ea5c9b2f07d; "
                "_lxsdk_cuid=16ea5c9b2f0c8-08cd26d4feb846-2393f61-1fa400-16ea5c9b2f07d; "
                "ctu=ddf4225da6cad41459a949b7b9de68c3403efd439d6753402e64673c2b6bf554; "
                "ua=dpuser_2360608922; "
                "_lxsdk_s=16f88085995-378-1eb-711%7C%7C290"
            ),
            "Host": "www.dianping.com",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    return s.content.decode()

css_font_dicts = {}
def decrypt_dazhong(content):
    global css_font_dicts
    css = 'http:' + re.findall('<link rel="stylesheet" type="text/css" href="(//s3plus.sankuai.com/v1/[^"]+)">', content)[0]
    if css not in css_font_dicts: css_font_dicts[css] = get_css_font_dict(css)
    css_dict, font_dict = css_font_dicts[css]
    def replace_func(e): return font_dict.get(css_dict.get(e.group(1)))
    return re.sub(r'<svgmtsi class="(.*?)"></svgmtsi>', replace_func, content)

if __name__ == '__main__':
    content = get_html_content()
    content = decrypt_dazhong(content) # 解密后的 html 文本，你可以注释/解开该行代码测试内容解密情况。

    # 若解密不正常，请求改请求头，因为请求头中可能有些参数过期了。
    from lxml import etree
    tree = etree.HTML(content)
    for x in tree.xpath('//div[3][@class="reviews-items"]/ul/li'):
        d = {}
        d["content"] = x.xpath('string(./div/div[@class="review-words Hide"])').strip()
        d["time"]    = x.xpath('string(./div/div/span[1][@class="time"])').strip()
        d["shop"]    = x.xpath('string(./div/div/span[2][@class="shop"])').strip()
        if "content" in d: d["content"] = re.sub(r'\s+',' ',d["content"])
        print('------------------------------ split ------------------------------')
        import pprint
        pprint.pprint(d)