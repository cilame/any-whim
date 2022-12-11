# 目前只有 sign 算法，没有 shield 算法的话仍然是什么也做不了。

import hashlib
from urllib.parse import quote,unquote
def get_sign(paramas_value):
    key = []
    for k,v in sorted(paramas_value.items()):
        key.append(k + '%3D' + quote(unquote(v)))
    key = ''.join(key)
    deviceId = paramas_value['deviceId']
    v1_2 = bytes(key, 'utf-8')
    v5_1 = ''
    v3_2 = 0
    v2 = 0
    v4_1 = bytes(deviceId, 'utf-8')
    while v2<len(v1_2):
        v5_1 = v5_1 + str(v1_2[v2] ^ v4_1[v3_2 ])
        v3_2 = (v3_2 + 1) % len(v4_1)
        v2 = v2 + 1
    md5hex = lambda word:hashlib.md5(word.encode()).hexdigest()
    sign = md5hex(md5hex(v5_1)+deviceId)
    return sign

url = (
    'https://www.xiaohongshu.com/api/sns/v9/search/notes'
    '?keyword=华语电影'
    '&filters=[]'
    '&sort='
    '&page=2'
    '&page_size=20'
    '&source=deep_link'
    '&search_id=1E9B47E3C07B552FB06B413A1C10D3DD'
    '&api_extra='
    '&page_pos=20'
    '&allow_rewrite=1'
    '&platform=android'
    '&deviceId=c72dae66-2e14-3acf-ba73-443629e13ebd'
    '&device_fingerprint=2019030717482409626a6348b0937df8333ecbe350d17a01f33916220174ec'
    '&device_fingerprint1=2019030717482409626a6348b0937df8333ecbe350d17a01f33916220174ec'
    '&versionName=6.5.0'
    '&channel=Store360'
    '&sid=session.1571800352331467986975'
    '&lang=zh-Hans'
    '&t=1571804596'
    '&fid=1568857415003f88488e6308f277d18d9ef4855443f7'
    '&sign=7bceb123df468d7d5aea3be60e4c39bb'
)
d = {
    'keyword'             :'华语电影',
    'filters'             :'[]',
    'sort'                :'',
    'page'                :'2',
    'page_size'           :'20',
    'source'              :'deep_link',
    'search_id'           :'1E9B47E3C07B552FB06B413A1C10D3DD',
    'api_extra'           :'',
    'page_pos'            :'20',
    'allow_rewrite'       :'1',
    'platform'            :'android',
    'deviceId'            :'c72dae66-2e14-3acf-ba73-443629e13ebd',
    'device_fingerprint'  :'2019030717482409626a6348b0937df8333ecbe350d17a01f33916220174ec',
    'device_fingerprint1' :'2019030717482409626a6348b0937df8333ecbe350d17a01f33916220174ec',
    'versionName'         :'6.5.0',
    'channel'             :'Store360',
    'sid'                 :'session.1571800352331467986975',
    'lang'                :'zh-Hans',
    't'                   :'1571804596',
    'fid'                 :'1568857415003f88488e6308f277d18d9ef4855443f7',
}
v = get_sign(d)
print(v)