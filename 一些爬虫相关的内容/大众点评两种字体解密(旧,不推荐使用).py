import re
import requests

def get_font_dict():
    # 生成请求参数函数
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
    font_dict = mk_font_dict('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/a611dc09acc5449dc110cb378b42c19c.svg')
    font_dict2 = mk_font_dict('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/6e016e5473bca0e3cedbed91f87a280c.svg')
    return font_dict, font_dict2

def get_css_dict():
    def mk_css_dict(url):
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
        css_dict = {}
        _exp1 = r'\.(.{5}){background:(.*?).0px (.*?).0px;}'
        _exp2 = r'\.(.{6}){background:(.*?).0px (.*?).0px;}'
        css_items = re.findall(_exp1, content, flags=re.S) or re.findall(_exp2, content, flags=re.S)
        for a,b,c in css_items:
            css_dict[a] = (int(b), int(c))
        return css_dict
    css_dict = mk_css_dict('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/6977f24cb12f17c2b63888656a6b52b9.css')
    css_dict2 = mk_css_dict('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/327710028a0b182c9cd3b898e835d819.css')
    return css_dict, css_dict2


def get_html_content():
    # 请配置头信息中的的 cookie 内容让正常的加密 HTML 文本结果返回，后再进行解密！！！！！！！！！
    def mk_url_headers():
        url = 'http://www.dianping.com/shop/9972787/review_all/p1'
        headers = {
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    return s.content.decode()

if __name__ == '__main__':
    css_dict, css_dict2 = get_css_dict()
    font_dict, font_dict2 = get_font_dict()
    content = get_html_content()# 请配置头信息中的的 cookie 内容让正常的加密 HTML 文本结果返回，后再进行解密！！！！！！！！！
    for svg in re.findall('<svgmtsi class="(.*?)"></svgmtsi>', content):
        font = font_dict.get(css_dict.get(svg)) or font_dict2.get(css_dict2.get(svg))
        content = re.sub(r'<svgmtsi class="%s"></svgmtsi>' % svg, font, content)
    print(content) # 解密后的 html 文本
