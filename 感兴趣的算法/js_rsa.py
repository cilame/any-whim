# 勉强用于一些网站的 rsa 加密处理
# 不过研究不够多，目前暂时处于勉强能用的阶段，没有非常详细验证效果。

# 有在 https://yhz3067.com/ 网站里面简单测试过
# 测试逻辑为
# 如果加密正常则，返回的结果为：  "{"sError":2,"sMsg":"请输入正确的用户名","aLinks":[]}"
# 如果加密错误则，返回的结果为：  "{"sError":2,"sMsg":"验证码错误!","aLinks":[]}"

import base64
from random import randint as rdi
def encode_rsa(key):
    bigint_n = 'B0AAFA4C9D388208E9F55B14DF04C8603D0CD81B7B65BBD669FA893096C985E33682FE7DEEE6500E1C4C6722C9855B6DD2E130F3672BEBA446B72D8DFFF2DD1F4E23D6BD728E267A9DC2C544C6680712884926D67AF74B74E5AD8298034D8C16FE8E5A37706EF5E447E423E69CA7FD3E47BBF7A9B137EF9B0310E2560E13D3C1'
    bigint_e = '10001'
    bigi_n = int(bigint_n, 16)
    bigi_e = int(bigint_e, 16)
    def padding(msg, len, bytelen=128):
        spa = bytelen - (len % bytelen) - 3
        return bytes([0x00, 0x02] + [rdi(1, 255) for _ in range(spa)] + [0x00]) + msg
    e = int.from_bytes(padding(key.encode(), len(key)), 'big')
    c = pow(e, bigi_e, bigi_n)
    p, q = [], hex(c)[2:]
    for i in range(len(q)//2):
        p.append(int(q[i*2:(i+1)*2], 16))
    return bytes(p)

def split_117(s):
    plen = int(len(s)/117) if len(s)%117 == 0 else int(len(s)/117)+1
    pack = []
    for i in range(plen):
        pack.append(s[i*117: (i+1)*117])
    return pack

s = '''{"username":"13999999919","loginpass":"111111","code":"7c5c648ca442d355658c57658576dd5b","vvccookie":"2e0ce0bedee40afe5abab31fa2eb590f"}'''
print(s)
# 按照每 117 个字符进行切割，然后对切割出的每个部分进行 pkcs1 填充，然后进行加密
for i in split_117(s):
    e = encode_rsa(i)
    v = base64.b64encode(e).decode()
    print(v)