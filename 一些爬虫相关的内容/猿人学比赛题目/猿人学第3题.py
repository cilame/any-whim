import json
import requests
def get_info(page):
    headers = {
        "Host": "match.yuanrenxue.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "yuanrenxue.project",
        "Accept": "*/*",
        "Origin": "http://match.yuanrenxue.com",
        "Referer": "http://match.yuanrenxue.com/match/3",
        "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    session = requests.session()
    session.headers = headers
    url = 'http://match.yuanrenxue.com/logo'
    session.get(url)
    s = session.get('http://match.yuanrenxue.com/api/match/3?page={}'.format(page))
    jsondata = json.loads(s.text)
    return jsondata

allvalues = []
for page in range(1,6):
    jsondata = get_info(page)
    values = [i.get("value") for i in jsondata['data']]
    allvalues.extend(values)
    print('page:{} --> values:{}'.format(page, values))

import collections
v = collections.Counter(allvalues)
v = sorted(v.items(), key=lambda i:-i[1])[0]
print('id:{} count:{}'.format(v[0], v[1]))

# 正常输出结果
# page:1 --> values:[2838, 7609, 8717, 6923, 5325, 4118, 8884, 8717, 2680, 3721]
# page:2 --> values:[8490, 3148, 6025, 8526, 8529, 6481, 9489, 6599, 5500, 8717]
# page:3 --> values:[185, 8498, 6102, 9222, 8717, 2008, 9827, 8717, 8224, 2929]
# page:4 --> values:[3762, 567, 672, 8717, 9524, 7159, 986, 505, 6535, 9491]
# page:5 --> values:[3612, 9095, 7357, 9307, 5650, 2109, 23, 8717, 2110, 2792]
# id:8717 count:7