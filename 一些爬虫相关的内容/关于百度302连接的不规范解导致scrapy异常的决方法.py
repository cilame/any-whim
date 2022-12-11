# 最近在使用百度生成的连接请求自动302转到新的页面时候发现一个问题
# 在某些情况下，个人在使用 scrapy 时候使用下面内容进行请求，返回的结果有部分不一样
# 在这里的百度在处理 302 的时候返回的信息并不正常，以下的测试代码(需打开fiddler的8888端口代理执行)执行后也能看出（以下结果在使用者的电脑中出现，有些环境则没有）
# 下面的两次结果中，百度直接返回的 Loc 后面并没有冒号，但是经过 fiddler 代理的却有，或许是因为 fiddler 自动对该 302 跳转返回的信息进行了修正
# 或许是测试者的电脑或者网络环境或者各种各样并未定义到的问题，在 requests 里可以很好的解决问题，但是在 scrapy 在解析时会出现一点代码逻辑上的错误
# 所以需要通过一些方式进行处理才能让 scrapy 能够正常执行。


# test.py
content = b'GET http://www.baidu.com/link?url=f7MmAcUgfna60gkWf8wcWcuRKLMi-tZU-jGIEiM09SC HTTP/1.1\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.9\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36\r\nHost: www.baidu.com\r\n\r\n'
import socket
def get_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostbyname('www.baidu.com'), 80))
    s.send(content)
    print('============','get_info','===========')
    print(s.recv(1024).decode('utf-8'))
    s.close()

def get_info_by_proxy():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8888))
    s.send(content)
    print('============','get_info_by_proxy','===========')
    print(s.recv(1024).decode('utf-8'))
    s.close()
get_info()
get_info_by_proxy()
# 下面是代码执行结果
'''
============ get_info ===========
HTTP/1.1 302 Found
Server:   
Date: Sat, 07 Dec 2019 07:30:05 GMT
Content-Type: text/html;charset=utf8
Content-Length: 154
Location: http://www.skycn.net/
Connection: keep-alive
Bdpagetype: 3
Loc
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Pragma: no-cache
Set-Cookie: BAIDUID=0C28F5C26E0D3E454815CD19D7DA517E:FG=1; max-age=31536000; expires=Sun, 06-Dec-20 07:30:17 GMT; domain=.baidu.com; path=/; version=1; comment=bd
Set-Cookie: BDSVRTM=0; path=/
Traceid: 1575703817063647309812477331591225194142
X-Ua-Compatible: IE=Edge,chrome=1
<html>
<head><title>302 Found</title></head>
<body bgcolor="white">
<center><h1>302 Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
============ get_info_by_proxy ===========
HTTP/1.1 302 Found
Server: 
Date: Sat, 07 Dec 2019 07:30:05 GMT
Content-Type: text/html;charset=utf8
Content-Length: 154
Location: http://www.skycn.net/
Connection: keep-alive
Bdpagetype: 3
Loc: 
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Pragma: no-cache
Set-Cookie: BAIDUID=0C28F5C26E0D3E451434CD25E907B4D8:FG=1; max-age=31536000; expires=Sun, 06-Dec-20 07:30:17 GMT; domain=.baidu.com; path=/; version=1; comment=bd
Set-Cookie: BDSVRTM=0; path=/
Traceid: 1575703817028851866610884419033367189592
X-Ua-Compatible: IE=Edge,chrome=1
'''



# scrapy 的处理方式是在直接通过 monkey patch 的方式修正 twisted 内部的处理方式
# scrapy 请求本身就是用 twisted 来进行底层的处理，所以在爬虫代码头部增加以下代码即可处理该问题
def lineReceived(self, line):
    if line[-1:] == b'\r': line = line[:-1]
    if self.state == u'STATUS': self.statusReceived(line); self.state = u'HEADER'
    elif self.state == u'HEADER':
        if not line or line[0] not in b' \t':
            if self._partialHeader is not None:
                _temp = b''.join(self._partialHeader).split(b':', 1)
                name, value = _temp if len(_temp) == 2 else (_temp[0], b'')
                self.headerReceived(name, value.strip())
            if not line: self.allHeadersReceived()
            else: self._partialHeader = [line]
        else: self._partialHeader.append(line)
import twisted.web._newclient
twisted.web._newclient.HTTPParser.lineReceived = lineReceived