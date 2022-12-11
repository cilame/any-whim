import re
import json
import base64
import requests

def get_info(page):
    def mk_url_headers(page):
        url = (
            'http://match.yuanrenxue.com/api/match/12'
            '?page={}'
            '&m={}'
        ).format(page, base64.b64encode('yuanrenxue{}'.format(page).encode()).decode())
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "yuanrenxue.project"
        }
        return url,headers
    url,headers = mk_url_headers(page)
    s = requests.get(url,headers=headers)
    return json.loads(s.text)

allvalues = []
for page in range(1,6):
    jsondata = get_info(page)
    values = [i.get("value") for i in jsondata['data']]
    allvalues.extend(values)
    print('page:{} --> values:{}'.format(page, values))

print('sum:{}'.format(sum(allvalues)))

# 正常输出结果
# page:1 --> values:[62, 4633, 2177, 6424, 6567, 956, 2474, 7846, 7787, 2789]
# page:2 --> values:[4542, 9173, 8246, 4449, 8026, 374, 4610, 2916, 9066, 2618]
# page:3 --> values:[5150, 2325, 5170, 986, 6206, 6412, 5985, 9476, 4302, 8450]
# page:4 --> values:[8955, 2762, 1846, 8320, 8179, 6651, 2149, 7217, 1572, 976]
# page:5 --> values:[1233, 8043, 5598, 9933, 4680, 324, 9866, 4169, 3414, 998]
# sum:247082