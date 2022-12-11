# 直接运行该脚本即可测试
# 开发环境 python3
# 依赖： pip install requests cryptography


import json, time, random, base64
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
# 3des/cbc
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


# 获取日期过滤下的“所有的最低过滤条件”
def get_filter_infos(data_filter):
    def mk_url_headers_body(data_filter):
        url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
        headers = { "User-Agent": "Chrome/79.0.3945.79 Safari/537.36", }
        body = {
            "pageId": "373c2d16890fff79fcdb9562eb2cddba",
            "groupFields": "s33,s39,s40",
            "queryCondition": json.dumps(data_filter),
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@leftDataItem",
            "__RequestVerificationToken": "IOsNq5KiGl5SS3YvWzn7TBF1"
        }
        return url,headers,body
    url,headers,body = mk_url_headers_body(data_filter)
    content = requests.post(url,headers=headers,data=body).text
    jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
    filter_infos = []
    for d in jsondata['result']['s33,s39,s40']:
        if d["childGroupFieldList"]:
            for i in d["childGroupFieldList"]:
                if i["childGroupFieldList"]:
                    for j in i["childGroupFieldList"]:
                        _d = {'count':d['count'], 'value':d['value']}
                        _i = {'count':i['count'], 'value':i['value']}
                        _j = {'count':j['count'], 'value':j['value']}
                        filter_infos.append([('s33', _d),('s39', _i),('s40', _j)])
                else:
                    _d = {'count':d['count'], 'value':d['value']}
                    _i = {'count':i['count'], 'value':i['value']}
                    filter_infos.append([('s33', _d),('s39', _i)])
        else:
            _d = {'count':d['count'], 'value':d['value']}
            filter_infos.append([('s33', _d)])
        return filter_infos


# 通过日期过滤条件和一条最细过滤条件获取该条件下“所有能搜索到的docid”
def get_list_info(data_filter, filter_info):
    def mk_url_headers_body(final_filter, page):
        url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
        headers = { "User-Agent": "Chrome/76.0.3809.132 Safari/537.36" }
        body = {
            "pageId": "373c2d16890fff79fcdb9562eb2cddba",
            "sortFields": "s50:desc",
            "ciphertext": create_ciphertext(),
            "pageNum": str(page),
            "pageSize": "15",
            "queryCondition": json.dumps(final_filter),
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
            "__RequestVerificationToken": rdn(24)
        }
        return url,headers,body
    final_filter = data_filter
    for k, v in filter_info:
        final_filter.append({'key':k, 'value':v['value']})
    cnt = int(filter_info[-1][-1]['count'])
    cnt = min((cnt//15+1 if cnt/15 > cnt//15 else cnt//15),  40) # 最大页码不超过40(每页15条的条件下的最大页码)
    packs = []
    for page in range(1, cnt+1):
        print('curr page:{}/{} {}'.format(page, cnt, final_filter))
        url,headers,body = mk_url_headers_body(final_filter, page)
        _data     = json.loads(requests.post(url,headers=headers,data=body).content)
        key       = _data['secretKey'].encode()
        iv        = ('%04d%02d%02d' % time.localtime()[:3]).encode()
        _encdata  = base64.b64decode(_data['result'].encode())
        encryptor = get_encryptor(key, iv)
        data = json.loads(encryptor.decrypt(_encdata))
        packs.extend(list(data['relWenshu']))
    return packs


# 通过 docid 直接获取到文书的内容
def get_info_by_docid(docId):
    def mk_url_headers_body(docId):
        url = 'https://wenshu.court.gov.cn/website/parse/rest.q4w'
        headers = { "User-Agent": "Chrome/76.0.3809.132 Safari/537.36" }
        body = {
            "docId": docId,
            "ciphertext": create_ciphertext(), # 该参数传递了时间信息(加密)被用于判断是否超时，所以需要该函数进行动态生成
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


# 这里使用的过滤逻辑是
# 1 首先通过固定日期获取细的过滤条件（获取的过滤条件是一个深度树）
# 2 然后通过“地区”进行细分，                         该处无法细分则直接抛出过滤条件
#   如果“地区”能往下细分到“高级法院”，则继续细分，     该处无法细分则直接抛出过滤条件
#   如果“高级法院”能往下细分到“地区法院”，则继续细分，  该处无法细分则直接抛出过滤条件
# 通常来说这样处理的细分已经是最方便处理的最细的细分，一般都不会超过100，
# 目前文书网能够接受的一次搜索最大只能获取600条内容，所以以目前的细分方式一般都能获取到全部的数据
# 由于一些判决是直接在“高级法院”处理，而“地方法院”没有相关记录，所以这部分的数据可能会丢失，
# 猜测“地方法院”的判决会传递到“高级法院”，所以高级法院能找到全部的“地方法院”的判决书，但是直接递交到高级法院的就无法在地方法院有记录
# 因为所有的过滤条件都最细细分到“地方法院”，所以“高级法院”的搜索会放弃，丢失比例预估是 5% 或更低(个人看数据量进行猜测的不严谨结论)。所以基本忽略即可。
def get_all_docid_by_oneday(day):
    data_filter = [{"key": "cprq","value": day+' TO '+day}]
    filter_infos = get_filter_infos(data_filter) # 通过日期获取所有的最细过滤条件
    all_docids = []
    for idx, filter_info in enumerate(filter_infos):
        data_filter = [{"key": "cprq","value": day+' TO '+day}] # 这里是处理之前搜索不到新内容的BUG。
        docids = get_list_info(data_filter, filter_info) # 通过过滤器获条件下，所有的 docid
        all_docids.extend(docids)
        # 下面这块代码仅作为测试用，这样可以只测试三条最细过滤条件过滤后的某一天的所有 docid，如果有需要请删除下面这块代码！
        print('使用时请注释掉该处 break 代码！！！！')
        if idx == 2: break
    return all_docids


if __name__ == '__main__':

    # 测试获取某天全部的 docid
    day = "2019-12-02"
    day_docids = get_all_docid_by_oneday(day) # 使用时请注释掉该函数内的某块代码
    print('docids number', len(day_docids))
    print(day_docids)

    # 测试通过 docid 获取内容
    content = get_info_by_docid('5fad74cd74c34f1bb166ab1801852b8e')
    print(content)

    # 如果上面两条测试都跑失败了，有可能加密已经过期了，看情况也可能是网站被其他爬虫流氓搞挂了，
    # 如果是跑着跑着出现数据获取到错误数据，请考虑以下是否是被封IP，是否是请求太快了，慢一点，给网站一条活路
    # 代码都详细到这种程度了，你应该能看懂了吧，迭代一下日期就能获取到旧数据了。
    # 如果你问我日期怎么迭代？我TM就干死你！