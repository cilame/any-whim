# 带有 dbgprint 的 map 解析器代码
# from html.parser import HTMLParser
# class Vparser(HTMLParser):
#     def __init__(self, *a, debug=False, **k):
#         super().__init__(*a, **k)
#         self.maps, self.curr, self.debug = {'info':{}, 'sub':[]}, 0, debug
#     def get_curr_map_sub(self):
#         tmap = self.maps['sub']
#         for _ in range(self.curr): tmap = tmap[-1]['sub']
#         return tmap
#     def get_curr_map_info(self):
#         tmap = self.maps['sub']
#         for _ in range(self.curr - 1): tmap = tmap[-1]['sub']
#         return None if self.curr == 0 else tmap[-1]['info']
#     def get_curr_map_infos(self):
#         infos, tmap = [], self.maps['sub']
#         for _ in range(self.curr - 1): 
#             tmap = tmap[-1]['sub']
#             infos.append(tmap[-1]['info'])
#         return None if self.curr == 0 else infos
#     def _init_starttag(self): self.get_curr_map_sub().append({'info':{}, 'sub':[]}); self.curr += 1
#     def _finish_endtag(self): self.curr -= 1
#     def _record_maps(self, tag, attrs=None): cinfo = self.get_curr_map_info(); cinfo['tag'], cinfo['attrs'] = tag, dict(attrs)
#     def _record_maps_data(self, data):
#         cinfos = self.get_curr_map_infos()
#         if cinfos: 
#             for cinfo in cinfos: cinfo['data'] = data if 'data' not in cinfo else cinfo['data'] + data
#     def _dbgprint(self, tag_or_data, attrs=None, mode=None):
#         if self.debug: # mode must in ['start', 'end', 'startend', 'data']
#             fmtstr = ' '.join(['{}={}'.format(repr(x),repr(y)) for x,y in attrs]) if attrs else ''
#             if mode == 'start':     fmtstr = '<%s%s>' % (tag, ' ' + fmtstr if len(fmtstr) else fmtstr)
#             if mode == 'end':       fmtstr = '</%s>' % tag
#             if mode == 'startend':  fmtstr = '<%s%s />' % (tag, ' ' + fmtstr if len(fmtstr) else fmtstr)
#             if mode == 'data':      fmtstr = tag_or_data
#             print(fmtstr, end='')
#     def handle_starttag(self, tag, attrs):
#         if tag in ['br', 'meta', 'link']: return self.handle_startendtag(tag, attrs)
#         self._init_starttag(); self._record_maps(tag, attrs); self._dbgprint(tag, attrs, mode='start')
#     def handle_endtag(self, tag): self._finish_endtag(); self._dbgprint(tag, mode='end')
#     def handle_startendtag(self, tag, attrs): self._init_starttag(); self._record_maps(tag, attrs); self._finish_endtag(); self._dbgprint(tag, attrs, mode='startend')
#     def handle_data(self, data): self._record_maps_data(data); self._dbgprint(data, mode='data')

# 以下为一个无依赖的简易的 xpath 解析器，代码已经压缩到了六十行内。
# 能支持简单的 xpath 语法，无法支持轴的语法。有非常多的缺陷，但是在非苛刻条件下用着还行就可以了。
# 简单的字符串抽取；简答的属性抽取；简单的字符串抽取；属性条件窗只支持这种且只能传一个：[@xxx="fff"]，可以看示例代码
import re
from html.parser import HTMLParser
class Vparser(HTMLParser):
    def __init__(s, *a, **k): super().__init__(*a, **k); s.maps = s.m = {'info':{'data':''}, 'sub':[]}; s.c = 0
    def _a(s, m):       [m.update({'m':m['m'][-1]['sub']}) for _ in range(s.c)]
    def _b(s, m, i):    (m.update({'m':m['m'][-1]['sub']}), i.append(m['m'][-1]['info']))
    def _c(s, m, i):    [s._b(m, i) for _ in range(s.c - 1)]
    def _d(s):          m = {}; m['m'] = s.m['sub']; s._a(m); return m['m']
    def _e(s, a=0):     m = {}; m['m'] = s.m['sub'];i = []; s._c(m, i); return i if a else m['m'][-1]['info']
    def _f(s):          s._d().append({'info':{'data':''}, 'sub':[]}); s.c += 1
    def _g(s, t, a=0):  c = s._e(); c['tag'], c['attrs'] = t, dict(a)
    def _h(s, c, d):    c.update({'data':d}) if 'data' not in c else c.update({'data':c['data'] + d})
    def _i(s, d):       return [s._h(c, d) for c in s._e(True)] if s._e(True) else 0
    def _j(s, t):       return True if t in ['br','meta','link'] else False
    def handle_starttag(s, t, a): s.handle_startendtag(t, a) if s._j(t) else (s._f(), s._g(t, a))
    def handle_endtag(s, t): s.c -= 1
    def handle_startendtag(s, t, a): s._f(); s._g(t, a); s.c -= 1
    def handle_data(s, d): s._i(d)
class Vnode:
    def __init__(self, mapsdict): self.maps = mapsdict
    def __repr__(self): r = self.maps['info'].get('data'); return "<class 'Vnode' data={}>".format(repr(r.strip()[:10])[:-1]+"...'" if r else None)
    def find_by_maps(self, maps, tag='*', attrs={}, depth=float('inf'), one=None):
        r = []
        def _a(s, t):       return all([i not in t for i in s.split('|')])
        def _b(s, n):       return (_a(s[1:],n) if s.startswith('*') else s != n) and s != '*'
        def _c(k, i, v):    return k not in i['attrs'] or _b(v, i['attrs'][k])
        def _d(n):          return any([_c(k, n['info'], v) for k,v in attrs.items()])
        def _e(n):          return not _d(n) and not _b(tag, n['info']['tag'])
        def _f(ns, d=0):    [(r.append(n) if _e(n) else 0, _f(n,d+1)) for n in ns['sub']] if d < depth else 0
        return _f(maps) or (([r[one]] if len(r) > one else []) if type(one) == int else r)
    def xpath(self, x):
        def _pc(k, m, d, n):
            x = float('inf') if k.startswith('//') else 1; o = re.findall(r'\d+', d); o = int(o[0]) if o else None
            p = r'@([a-zA-Z_][a-zA-Z_0-9]+) *= *"([^"]+)"'; q = p.replace('"',"'"); b = p.split(' ',1)[0]+'( *)$'
            w = re.findall(p, n) + re.findall(q, n) + [(x, '*') for x,y in re.findall(b, n)]
            r1 = ('r', dict(w)) if w else (None, {}); c = re.findall(r'@([a-zA-Z_][a-zA-Z_0-9]+) *$', m)
            r2 = ('c', ['attrs', c[0]]) if c and c[0] == m.strip('@ ') else (('c', ['data']) if m.strip() == 'text()' else (None, {}))
            return x, o, m, r1 if r1[0] else r2
        p = re.findall(r'(//?)([^/[\[\]]+)(\[ *\d+ *\])?(\[[^/\[\]]+\])?', x); r = {}; ms = [self.maps]
        for i, (k, m, d, n) in enumerate(p, 1):
            r[i] = []; d, o, m, (g, a) = _pc(k, m, d, n)
            if (i != len(p) or i == 1): [r[i].extend(self.find_by_maps(s, m, attrs=a, depth=d, one=o)) for s in ms]
            elif g == 'r':              [r[i].extend(self.find_by_maps(s, m, attrs=a, depth=d, one=o)) for s in ms]
            else: [r[i].append(s['info']['attrs'].get(a[1]) if a[0] =='attrs' else (s['info']['data'] if a[0] =='data' else None) if a else s) for s in ms]
            ms = r[i]; r[i - 1] = None
        return [Vnode(i) if type(i) == dict else i for i in ms]
class VHTML:
    def __init__(self, hc): self.pr = Vparser(); self.pr.feed(hc); self.root = Vnode(self.pr.maps)
    def xpath(self, x): return self.root.xpath(x)




if __name__ == '__main__':
    html_content = r'''
        <HTML>
            <head>
                <meta charset="utf-8" />
                <title>在线JSON校验格式化工具（Be JSON）</title>
                <link rel='dns-prefetch' href='//www.bejson.com' />
            </head>
            <body>
                <!-- test html parser -->
                <img src='http://asdfasdf.jpg' />
                <div id="123" class="asdf">
                有点可怕
                    <p aaa='fff'>你好啊兄弟</p>
                </div>
                <p class="asdf">
                    Some 
                    <a href="#">有点可怕html1</a>
                    <a href="#">html2</a>
                    HTML&nbsp;tutorial...<br/>END
                </p>
                <p>
                    Some
                    <a href="http://www.asdf1.com" class="fff">html3</a>
                    <a href="http://www.asdf2.com" class="fff">html4</a>
                    <a>html4</a>
                    asdfasdfasdf<br/>END
                    <div>
                        <a href="#123">html2 </a>
                    </div>
                </p>
            </body>
        </html>
    '''
    v = VHTML(html_content)
    x = '//p[@class="asdf"]/a/text()'
    print('-------------')
    print('[xpath]:', x)
    print(v.xpath(x))

    x = '//p'
    print('-------------')
    print('[xpath]:', x)
    for idx, i in  enumerate(v.xpath(x)):
        print(idx,'======',i.xpath('/a'))

    x = '//a/text()'
    print('-------------')
    print('[xpath]:', x)
    print(v.xpath(x))
    
    x = '//a[@class="fff"]/@href'
    print('-------------')
    print('[xpath]:', x)
    for i in v.xpath(x):
        print(i)


    import re, json
    from urllib import request, parse
    from urllib.parse import quote, unquote, urlencode

    def mk_url_headers():
        def quote_val(url): return re.sub('=([^=&]+)',lambda i:'='+quote(unquote(i.group(1))), url)
        url = (
            'https://www.baidu.com/sf/vsearch'
            '?wd=sparklehorse inurl:youku'
            '&pd=video'
            '&tn=vsearch'
            '&lid=978ba643001c9b66'
            '&ie=utf-8'
            '&rsv_spt=4'
            '&rsv_bp=1'
            '&f=8'
            '&oq=123+inurl:youku'
            '&rsv_pq=978ba643001c9b66'
            '&rsv_t=f2bckJx2la/O4hoy93/BoWizeR4VOPtsL5xyYOo/eQBC1QEchv3ORwngwEZcfQ'
        )
        url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers

    method = 'GET'
    url, headers = mk_url_headers()
    body = None
    r = request.Request(url, method=method)
    for k, v in headers.items():
        if k.lower() == 'accept-encoding': continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    s = request.urlopen(r)
    print(url)

    content = s.read()
    parser = Vparser()
    print('start')
    v = VHTML(content.decode())
    for i in v.xpath('//a/@href'): print(i)
    print('---- split ----')
    for i in v.xpath('//div/div/span[1][@class="wetSource"]/text()'): print(i)
    print('end')