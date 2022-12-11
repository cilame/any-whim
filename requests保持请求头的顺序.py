import requests

url = "xxx"
headers = {
    "Host": "match.yuanrenxue.com",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Origin": "http://match.yuanrenxue.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "*/*",
    "Referer": "http://match.yuanrenxue.com/match/3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
# 先session
session=requests.Session()
# 后session clear，clear这个是比较关键的写法。
session.headers.clear()
session.headers.update(
    headers
)
resp=session.post(url)