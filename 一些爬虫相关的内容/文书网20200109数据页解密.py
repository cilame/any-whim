import json, time, random, base64

# pip install requests cryptography
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# 3des, cbc
def get_encryptor(key, iv=None):
    algoer = algorithms.TripleDES(key)
    cipher = Cipher(algoer, modes.CBC(iv), backend=default_backend())
    def enc(bitstring):
        padder    = padding.PKCS7(algoer.block_size).padder()
        bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()
    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata     = decryptor.update(bitstring) + decryptor.finalize()
        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
        ddata     = unpadder.update(ddata) + unpadder.finalize()
        return ddata
    class f:pass
    f.encrypt, f.decrypt = enc, dec
    return f

def rdn(length):
    temp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join([random.choice(temp) for i in range(length)]).encode()

def create_ciphertext():
    key  = rdn(24)
    iv   = ('%04d%02d%02d' % time.localtime()[:3]).encode()
    data = str(int(time.time()*1000)).encode()
    encryptor = get_encryptor(key, iv)
    data =  (key + iv + base64.b64encode(encryptor.encrypt(data))).decode()
    return ' '.join([bin(ord(i))[2:] for i in data])

def get_info_by_docid(docId):
    def mk_url_headers_body(docId):
        url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
        headers = { "User-Agent": "Chrome/76.0.3809.132 Safari/537.36" }
        body = {
            "docId": docId,
            "ciphertext": create_ciphertext(), # 该参数传递了时间信息(加密)被用于服务器判断请求是否过期，所以需要该函数进行动态生成
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
            "__RequestVerificationToken": rdn(24)
        }
        return url,headers,body
    url,headers,body = mk_url_headers_body(docId)
    _data     = json.loads(requests.post(url,headers=headers,data=body).content)
    key       = _data['secretKey'].encode()
    iv        = ('%04d%02d%02d' % time.localtime()[:3]).encode()
    _encdata  = base64.b64decode(_data['result'].encode())
    encryptor = get_encryptor(key, iv)
    return json.loads(encryptor.decrypt(_encdata))

if __name__ == '__main__':
    s = get_info_by_docid("adb77f453fa84556a8afaaba00c0fa28")
    print(s)
