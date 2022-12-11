import re
import time
import hashlib

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
def get_m3u8_pbody(script):
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



import requests

import html
import json
from urllib.parse import quote, unquote, urlencode
def get_m3u8_url(url):
    def mk_url_headers(url):
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    def mk_url_headers_body(pbody):
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
            "referer": "https://v.douyu.com/show/a4Jj7l23PrBWDk01",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        return url,headers,pbody
    url, headers = mk_url_headers(url)
    s = requests.get(url,headers=headers) 
    pbody = get_m3u8_pbody(html.unescape(s.text))
    url, headers, body = mk_url_headers_body(pbody)
    s = requests.post(url,headers=headers,data=body) 
    jsondata = json.loads(s.content)
    return jsondata


if __name__ == '__main__':
    requrl = 'https://v.douyu.com/show/a4Jj7l23PrBWDk01'
    jsondata = get_m3u8_url(requrl)

    import pprint
    pprint.pprint(jsondata)