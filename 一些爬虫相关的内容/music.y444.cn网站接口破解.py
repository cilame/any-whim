
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
def get_encryptor(key, iv=None):
    algoer = algorithms.AES(key) #若要使用DES这里改成TripleDES
    mode   = modes.CBC(iv)       #模式若是ecb则为 modes.ECB(), 其余模式均为一个参数 mode.***(iv)
    cipher = Cipher(algoer, mode, backend=default_backend())
    def enc(bitstring):
        padder    = padding.PKCS7(algoer.block_size).padder()
        bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()
    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata     = decryptor.update(bitstring) + decryptor.finalize()
        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
        return unpadder.update(ddata) + unpadder.finalize()
    class f:pass
    f.encrypt = enc
    f.decrypt = dec
    return f

def enc_post_params(real_params):
    key         = b'KCdQHKAZrNebiC5r'
    iv          = b'0102030405060708'
    data        = real_params.encode()
    encryptor   = get_encryptor(key, iv)
    return base64.b64encode(encryptor.encrypt(data))

def dec_retrun_info(data):
    key         = b'2wVGQU6CMFpZzMQX'
    iv          = b'0102030405060708'
    data        = data.encode()
    db64        = base64.b64decode(data)
    encryptor   = get_encryptor(key, iv)
    v = encryptor.decrypt(db64).decode()
    jsondata = json.loads(v)
    return jsondata






# 通过关键词获取歌曲列表信息
import re, json
from urllib import request, parse
from urllib.parse import unquote, quote, urlencode
def mk_url_headers(key):
    def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
    url = (
        'http://music.y444.cn/api/v1/search/v3/'
        '?keyword={}'
        '&page=1'
        '&size=10'
        '&src=wyy'
    ).format(key)
    url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
    headers = { "User-Agent": "Chrome/84.0.4147.125 Safari/537.36"}
    return url,headers
def myget(url, headers):
    r = request.Request(url, method='GET')
    for k, v in list(headers.items()):
        if k.lower() == 'accept-encoding': 
            headers.pop(k); continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r)
key = '恐怖'
url, headers = mk_url_headers(key)
content = myget(url, headers).read()
jsondata = json.loads(content)
jsondata = dec_retrun_info(jsondata['data'])
import pprint
pprint.pprint(jsondata)





# 通过歌曲id信息获取音乐真实地址信息
import re, json
from urllib import request, parse
from urllib.parse import urlencode
def mk_url_headers_body(songid):
    url = 'http://music.y444.cn/api/v1/jx/v4/'
    headers = { "User-Agent": "Chrome/84.0.4147.125 Safari/537.36" }
    body = { "params": enc_post_params(json.dumps({"id":songid,"q":"128","src":"wyy","play":True})), # q代表质量固定即可，这里的src就是网易云固定即可，play固定即可，所以这里你只需要音乐id的参数即可
             "sec_key": "SMGnQH2eEpzq9CNl8QNA86De2yjyRxWltD/KCeg+i9SjR3o+QjgUPPeKIy+Batt3cNQr3wBrqTAvn7SccdK7QyPRlOW6aFeg9dxGpEYQEBwKjqYqz7BUPvijJVbYkE+/HRaJpLutephcENsy1zKeRk95ciyO6MLvtRJG7mi3an0=" }
    body = urlencode(body).encode('utf-8')
    return url,headers,body
def mypost(url, headers, body):
    r = request.Request(url, method='POST')
    for k, v in list(headers.items()): r.add_header(k, v)
    opener = request.build_opener(request.ProxyHandler(None))
    return opener.open(r, data=body)
songid = 414817
url, headers, body = mk_url_headers_body(songid)
content = mypost(url, headers, body).read()
jsondata = json.loads(content)
jsondata = dec_retrun_info(jsondata['data'])
import pprint
pprint.pprint(jsondata)

real_song_url = jsondata['url']['local']
print(real_song_url)