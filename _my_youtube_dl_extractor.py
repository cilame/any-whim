# coding: utf-8
from __future__ import unicode_literals

import re
import urllib.parse
import json, time, html, hashlib, traceback

from .common import InfoExtractor


# 该插件为 youtube-dl 的补充插件，包含 yy 回放视频下载方式，斗鱼show视频下载方式
# yy视频历史视频下载，适合如下连接格式
#     eg. https://www.yy.com/x/15012_2464989902_22490906_1585798203199
# 虎牙视频下载，适合如下格式连接
#     eg. https://v.huya.com/play/216591840.html
# 斗鱼show视频下载，适合如下连接格式
#     eg. https://v.douyu.com/show/a4Jj7l23PrBWDk01
# 一直播视频下载，适用于如下连接格式（该处网站视频似乎都有点大，七八个小时的直播视频都放一个m3u8地址，属实抽象）
#     eg. http://www.yizhibo.com/l/2SEFmIKoZzT1mruj.html
# 新华网视频下载插件，适用于如下连接格式
#     eg. http://vod.xinhuanet.com/v/vod.html?vid=536626
# 新华网视频下载插件，适用于如下连接格式
#     eg. http://www.xinhuanet.com/video/2018-08/28/c_129941452.htm

# 使用前须知，
# 1 将该脚本命名为 _my_extractor.py 并放在 youtube_dl/extractor 文件夹下
# 2 请找到 youtube_dl/extractor 文件夹下的 extractors.py 文件
#   并在最后添加一行内容 from ._my_extractor import YYRecordIE, DouyuShowIE, HuyaIE, XinHuaNetIE, XinHuaNet2IE, YiZhiBoIE


# yy视频历史视频下载，适合如下连接格式
# eg. https://www.yy.com/x/15012_1101280606_54880976_1595811603845
class YYRecordIE(InfoExtractor):
    IE_NAME = 'YYRecordIE'
    IE_DESC = 'YYRecordIE video downloader.'
    _VALID_URL = r'https://www\.yy\.com/x/([^/+])'

    def _real_extract(self, url):
        def get_real_url_by_simple_url(self, url):
            uid = re.findall(self._VALID_URL, url)[0]
            page = self._download_webpage(url, uid)
            m3u8 = re.findall(r'video: *"(http://record\.vod\.huanjuyun\.com/xcrs/[^\.]+\.m3u8)"', page)[0]
            return uid, m3u8

        uid, url = get_real_url_by_simple_url(self, url)
        # 对于 youtube-dl 工具而言，该函数返回的参数是一个字典，至少要包括 id，title，url 这三个key的字典。
        if url:
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
                'ext':      'mp4',
            }
        else:
            print(traceback.format_exc())


# 虎牙视频下载，适合如下格式连接
# eg. https://v.huya.com/play/216591840.html
class HuyaIE(InfoExtractor):
    IE_NAME = 'HuyaIE'
    IE_DESC = 'HuyaIE video downloader.'
    _VALID_URL = r'https://v\.huya\.com/play/(\d+)\.html'

    def _real_extract(self, url):
        def mk_url_headers(videoId):
            url = (
                'https://liveapi.huya.com/moment/getMomentContent'
                '?callback=jQuery1124005428239881979824_1585902134610'
                '&videoId={}'
                '&uid='
                '&_=1585902134630'
            ).format(videoId)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers

        uid = re.findall(self._VALID_URL, url)[0]
        url, headers = mk_url_headers(uid)

        page = self._download_webpage(url, uid, headers=headers)
        jsondata = json.loads(page[page.find('{'):page.rfind('}')+1])
        url = None
        definitions = jsondata['data']['moment']['videoInfo']['definitions']
        for d in definitions:
            if d.get('defName') == '原画':
                url = d.get('url') or d.get('m3u8')
        if not url:
            for d in definitions:
                url = d.get('url') or d.get('m3u8')
                if url:
                    break
        # 对于 youtube-dl 工具而言，该函数返回的参数是一个字典，至少要包括 id，title，url 这三个key的字典。
        if url:
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
                'ext':      'mp4',
            }
        else:
            print(traceback.format_exc())


# 斗鱼show视频下载，适合如下连接格式
# eg. https://v.douyu.com/show/a4Jj7l23PrBWDk01
class DouyuShowIE(InfoExtractor):
    IE_NAME = 'DouyuIE'
    IE_DESC = 'DouyuIE video downloader.'
    _VALID_URL = r'https://v\.douyu\.com/show/([a-zA-Z0-9]+)'

    def _real_extract(self, url):
        def mk_url_headers(url):
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        def mk_url_headers_body(referer, pbody):
            url = (
                'https://v.douyu.com/api/stream/getStreamUrl'
            )
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cookie": (
                    "acf_did=dbbbd666b6681de09151847100001501; "
                    "dy_did=dbbbd666b6681de09151847100001501; "
                    "Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1589354641,1589354653"
                ),
                "origin": "https://v.douyu.com",
                "pragma": "no-cache",
                "referer": referer,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            return url,headers,pbody

        uid = re.findall(self._VALID_URL, url)[0]
        url, headers = mk_url_headers(url)
        page = self._download_webpage(url, uid, headers=headers)
        pbody = self.get_m3u8_pbody(html.unescape(page))
        url, headers, body = mk_url_headers_body(url, pbody)
        page = self._download_webpage(url, uid, headers=headers, data=urllib.parse.urlencode(body).encode())
        jsondata = json.loads(page)
        thumb_video = jsondata['data']['thumb_video']
        if 'normal' in thumb_video:
            url = thumb_video['normal']['url'] # 优先 normal 类型视频
        else:
            for key in thumb_video:
                url = thumb_video[key]['url'] # 否则按照字典顺序随便拿一条就好了，懒得想什么优先级
                break

        # 对于 youtube-dl 工具而言，该函数返回的参数是一个字典，至少要包括 id，title，url 这三个key的字典。
        if url:
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
                'ext':      'mp4',
            }
        else:
            print(traceback.format_exc())

    @staticmethod
    def get_m3u8_pbody(script):
        def _rot(num, rnum, side):
            bnum = bin(((1 << 32) - 1) & num)[2:]
            s = [None] * 32
            for idx, i in enumerate('{:>032s}'.format(bnum[-32:])):
                s[idx] = '0' if i == '0' else '1'
            if side == 'left':
                s.extend(['0'] * rnum)
                s = s[-32:]
            elif side == 'right':
                s = ['0'] * rnum + s
                s = s[:32]
            if s[0] == '1':
                for i in range(1,32):
                    s[i] = '1' if s[i] == '0' else '0'
                v = -int(''.join(s[1:]), 2)-1
            else:
                v = int(''.join(s),2)
            return v
        def limitint(num):
            bnum = bin(((1 << 32) - 1) & num)[2:]
            s = [None] * 32
            for idx, i in enumerate('{:>032s}'.format(bnum[-32:])):
                s[idx] = '0' if i == '0' else '1'
            if s[0] == '1':
                for i in range(1,32):
                    s[i] = '1' if s[i] == '0' else '0'
                v = -int(''.join(s[1:]), 2)-1
            else:
                v = int(''.join(s),2)
            return v
        def rotleft(num, rnum):
            return _rot(num, rnum, 'left')
        def rotright(num, rnum):
            return _rot(num, rnum, 'right')

        def get_hide_funcstring(s):
            rk = list(map(int, re.findall(r'var rk=\[((?:\d+,)*(?:\d+))\]', s)[0].split(',')))
            k2 = list(map(lambda x:int(x, 16), re.findall(r'var k2=\[((?:0x[0-9a-z]+,)*(?:0x[0-9a-z]+))\]', s)[0].split(',')))
            v = list(map(lambda x:int(x, 16), re.findall(r'\[((?:0x[0-9a-z]+,)*(?:0x[0-9a-z]+))\]', s)[0].split(',')))
            lk = list(map(lambda x:int(x, 16), re.findall(r'var lk=\[((?:0x[0-9a-z]+,)*(?:0x[0-9a-z]+))\]', s)[0].split(',')))
            k = list(map(lambda x:int(x, 16), re.findall(r'var k=\[((?:0x[0-9a-z]+,)*(?:0x[0-9a-z]+))\]', s)[0].split(',')))
            temp1 = int(re.findall(r'v\[O\]\^=(0x[a-z0-9]+)', s)[0], 16)

            flist = re.findall(r'v\[(\d+)\]([+-\^]?)=([^;]+);', s)[:-1]
            temp2 = int(re.findall(r'v\[0\]\^=(0x[a-z0-9]+)', s)[0], 16)
            for i in range(len(v)):
                v[i] ^= temp1
            def parse2(f, v, lk):
                a,b = f.split('|')
                if '<' in a: (x,y),p1 = a.split('<<'),  '<'
                if '>' in a: (x,y),p1 = a.split('>>>'), '>'
                if '<' in b: (m,n),p2 = b.split('<<'),  '<'
                if '>' in b: (m,n),p2 = b.split('>>>'), '>'
                x = v[int(re.findall(r'v\[(\d+)\]', x)[0])]
                m = v[int(re.findall(r'v\[(\d+)\]', m)[0])]
                y =      lk[int(re.findall(r'lk\[(\d+)\]', y)[0])] % 16
                n = 32 - lk[int(re.findall(r'lk\[(\d+)\]', n)[0])] % 16
                if p1 == '<': r1 = rotleft(x, y)
                if p1 == '>': r1 = rotright(x, y)
                if p2 == '<': r2 = rotleft(m, n)
                if p2 == '>': r2 = rotright(m, n)
                return r1 | r2
            for i,m,f in flist[:-1]:
                if f.count('v') == 0:
                    r = lk[int(re.findall(r'lk\[(\d+)\]', f)[0])]
                else:
                    r = parse2(f, v, lk)
                if m == '-': v[int(i)] -= r
                if m == '+': v[int(i)] += r
                if m == '^': v[int(i)] ^= r
                if m == '':  v[int(i)] =  r
            I = 0
            while (I < len(v)):
                v0 = v[I] ^ k2[0]
                v1 = v[I + 1] ^ k2[1]
                d = 0x9E3779B9
                sum = d * rk[I // 2]
                for i in range(rk[I // 2]):
                    v1 -= limitint(limitint(rotleft(v0, 4) ^ rotright(v0, 5)) + v0) ^ limitint(sum + k[(sum >> 11) & 3]);
                    sum -= d;
                    sum = limitint(sum)
                    v0 -= limitint(limitint(rotleft(v1, 4) ^ rotright(v1, 5)) + v1) ^ limitint(sum + k[sum & 3]);
                v[I] = v0 ^ k2[1]
                v[I + 1] = v1 ^ k2[0]
                I += 2
            O = len(v) - 1
            while (O > 0):
                v[O] ^= v[O - 1]
                O -= 1
            v[0] ^= temp2
            r = []
            for i in range(len(v)):
                a,b,c,d = v[i] & 0xff, v[i] >> 8 & 0xff, v[i] >> 16 & 0xff, v[i] >> 24 & 0xff
                r.extend([a,b,c,d])
            return bytes(r).decode(errors='ignore')

        def get_sign(point_id, ltime, fixed_value, timestamp, hide_funcstring):
            k2 = list(map(lambda x:int(x, 16), re.findall(r'var k2=\[((?:0x[0-9a-z]+,)*(?:0x[0-9a-z]+))\]', hide_funcstring)[0].split(',')))
            flist = re.findall(r're\[(\d+)\]([+-\^]?)=([^;]+);', hide_funcstring)
            cb = str(point_id) + str(fixed_value) + str(timestamp) + ltime
            rb = hashlib.md5(cb.encode()).hexdigest()
            _re = [None] * 4
            for i in range(4):
                a = (int(rb[i*8+0:i*8+2], 16) & 0xff)
                b = (rotleft(int(rb[i*8+2:i*8+4], 16), 8) & 0xff00)
                c = rotright(rotleft(int(rb[i*8+4:i*8+6], 16), 24), 8)
                d = rotleft(int(rb[i*8+6:i*8+8], 16), 24)
                _re[i] = a | b | c | d
            for I in range(2):
                v0 = _re[I * 2]
                v1 = _re[I * 2 + 1]
                sum = 0
                i = 0
                delta = 0x9e3779b9
                for i in range(32):
                    sum += delta
                    sum = limitint(sum)
                    v0 += limitint(limitint(rotleft(v1, 4) + k2[0]) ^ limitint(v1 + sum) ^ limitint(rotright(v1, 5) + k2[1]))
                    v1 += limitint(limitint(rotleft(v0, 4) + k2[2]) ^ limitint(v0 + sum) ^ limitint(rotright(v0, 5) + k2[3]))
                _re[I * 2] = v0
                _re[I * 2 + 1] = v1
            def parse2(f, v, lk):
                a,b = f.split('|')
                if '<' in a: (x,y),p1 = a.split('<<'),  '<'
                if '>' in a: (x,y),p1 = a.split('>>>'), '>'
                if '<' in b: (m,n),p2 = b.split('<<'),  '<'
                if '>' in b: (m,n),p2 = b.split('>>>'), '>'
                x = v[int(re.findall(r're\[(\d+)\]', x)[0])]
                m = v[int(re.findall(r're\[(\d+)\]', m)[0])]
                y =      lk[int(re.findall(r'k2\[(\d+)\]', y)[0])] % 16
                n = 32 - lk[int(re.findall(r'k2\[(\d+)\]', n)[0])] % 16
                if p1 == '<': r1 = rotleft(x, y)
                if p1 == '>': r1 = rotright(x, y)
                if p2 == '<': r2 = rotleft(m, n)
                if p2 == '>': r2 = rotright(m, n)
                return r1 | r2
            for i,m,f in flist:
                # print(f)
                if f.count('re') == 0:
                    r = k2[int(re.findall(r'k2\[(\d+)\]', f)[0])]
                else:
                    r = parse2(f, _re, k2)
                if m == '-': _re[int(i)] -= r
                if m == '+': _re[int(i)] += r
                if m == '^': _re[int(i)] ^= r
                if m == '':  _re[int(i)] =  r
            hc = list('0123456789abcdef')
            for i in range(4):
                s = ''
                for j in range(4):
                    s += hc[(_re[i] >> (j * 8 + 4)) & 15] + hc[(_re[i] >> (j * 8)) & 15]
                _re[i] = s
            return ''.join(_re)
        point_id    = re.findall(r'"point_id":(\d+)', script)[0]
        ltime       = re.findall(r'var vdwdae325w_64we = "(\d+)";', script)[0]
        timestamp   = int(time.time())
        vid         = re.findall(r'"vid":"([^"]+)"', script)[0]
        sign        = get_sign(point_id, ltime, 'dbbbd666b6681de09151847100001501', timestamp, get_hide_funcstring(script))
        d = {}
        d['v']    = ltime
        d['did']  = 'dbbbd666b6681de09151847100001501'
        d['tt']   = timestamp
        d['sign'] = sign
        d['vid']  = vid
        return d


# 一直播视频下载，适用于如下连接格式（该处网站视频似乎都有点大，七八个小时的直播视频都放一个m3u8地址，确实有点抽象）
# eg. http://www.yizhibo.com/l/2SEFmIKoZzT1mruj.html
class YiZhiBoIE(InfoExtractor):
    IE_NAME = 'YiZhiBoIE'
    IE_DESC = 'YiZhiBoIE video downloader.'
    _VALID_URL = r'http://www\.yizhibo\.com/l/([^/\?]+)\.html'

    def _real_extract(self, url):
        uid = re.findall(self._VALID_URL, url)[0]
        page = self._download_webpage(url, uid)
        url = re.findall(r'play_url:"([^"]+\.m3u8)"', page)[0]

        page = self._download_webpage(url, uid)
        number = len(re.findall('#EXTINF:', page))
        print('需要下载 {} 片数据'.format(number))
        # 如果下载片过大，请酌情在这里进行限制调整

        # 对于 youtube-dl 工具而言，该函数返回的参数是一个字典，至少要包括 id，title，url 这三个key的字典。
        if url:
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
                'ext':      'mp4',
            }
        else:
            print(traceback.format_exc())


# 新华网视频下载插件，适用于如下连接格式
# eg. http://vod.xinhuanet.com/v/vod.html?vid=536626
class XinHuaNetIE(InfoExtractor):
    IE_NAME = 'xinhuanet'
    IE_DESC = 'xinhuanet video downloader.'
    _VALID_URL = r'http://vod\.xinhuanet\.com/v/vod\.html\?vid=\d+'

    def _real_extract(self, url):
        def get_real_url_by_simple_url(self, url):
            def _mk_gcid_url(url):
                u = 'http://vod.xinhuanet.com/vod_video_js/%d/%d.js'
                v = int(url.rsplit('=')[1])
                uid = str(v)
                v = u % (int(v/1000),v) 
                # 混肴后的js源代码里面的函数方法：
                # 源代码："http://vod.xinhuanet.com/vod_video_js/"+Math.floor(parseInt(a)/1E3)+"/"+a+".js";
                # 源代码里面的 a 代表了该视频页的数字vid。 通过这个地址进一步获取 gcid 信息后续再继续处理。
                return v,uid

            gurl, uid = _mk_gcid_url(url)
            page = self._download_webpage(gurl, uid)
            gcid = re.findall(r"subdata:\[\{lurl:'http://:8080/0/([^/]{40})'\}\]",page)

            if gcid: gcid = gcid[0].upper()
            else: return 'gcid failed,'+gurl,None

            # 通过 gcid 拼接下面的地址可以获取到一些类似js脚本的HTML文本，里面有真实的视频url地址信息
            url = 'http://p2s.xinhuanet.com/getCdnresource_flv?gcid=' + gcid
            page = self._download_webpage(url, uid)
            vurl = re.findall('{ip:"([^"]+)",port:(\d+),path:"([^"]+)"}',page)

            if vurl: vurl = vurl[0]
            else: return 'get realurl failed,'+url,None

            def _get_real_url(vurl):
                # 对通过 gcid 获取的文本找到的信息拼接视频真实 url.
                # vurl 数据样例： ('vodfile12.news.cn', '8080', '/data/cdn_transfer/5C/FB/5cf3d08723ca6a481eb81a572505af7dcca381fb.mp4')
                # 这里没有使用port参数原因是测试得出的结论（8080端口无法使用，用默认80端口就能获取视频，所以不需要使用该port）
                url = 'http://' + vurl[0] + '/' + vurl[2]
                return url
            return uid, _get_real_url(vurl)
        uid, url = get_real_url_by_simple_url(self, url)

        # 对于 youtube-dl 工具而言，该函数返回的参数是一个字典，至少要包括 id，title，url 这三个key的字典。工具会通过这个视频真实url进行下载。
        # 另外，通过给与的url: http://.../vod.html?vid=532276 这个视频地址无法获取更多视频详细信息，甚至连标题信息都没有
        # 所以我把 title和 id都赋值为uid了，下载文件的名字默认为 "%s-%s" % (id, title)
        if url:
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
            }
        else:
            # 如果获取真实url失败，则我写的代码里，uid里面回传了简单的错误信息
            # 主要可能是视频不存在了，如果有其他异常可能是正则匹配问题，会打印一下问题出现的地址
            print(traceback.format_exc())


# 新华网视频下载插件，适用于如下连接格式
# eg. http://www.xinhuanet.com/video/2018-08/28/c_129941452.htm
class XinHuaNet2IE(InfoExtractor):
    IE_NAME = 'xinhuanet'
    IE_DESC = 'xinhuanet video downloader.'
    _VALID_URL = r'https?://www\.xinhuanet\.com/video/[^/]+/[^/]+/(?P<id>[^\.]+)\.htm'

    def _real_extract(self, url):
        # 原本计划是从该新闻页面找到嵌套在里面的视频页，然后通过视频页解析方法进一步获取真实地址的
        # 结果发现该页面上直接包含了真实的视频url地址，这设计很真实。真实~ 实在是太真实了~，连跳板都省了。
        m = re.match(self._VALID_URL, url)
        uid = m.group('id')
        page = self._download_webpage(url,uid)
        r_uid = re.findall('http://vod\.xinhuanet\.com/v/vod\.html\?vid=(\d+)',page)
        r_url = re.findall('(?:vodfile)[^<]+(?:mp4)',page)
        if r_uid and r_url:
            uid,url = r_uid[0],'http://' + r_url[0]
            return {
                'id':       uid,
                'title':    uid,
                'url':      url,
            }
        else:
            print(traceback.format_exc())

