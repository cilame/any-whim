import re, json
from urllib.parse import parse_qsl
from wsgiref.simple_server import make_server, WSGIServer

import socketserver
class WS(socketserver.ThreadingMixIn, WSGIServer): pass

class Router:
    def __init__(self, route):
        self.route = route
    def parse(self, environ):
        pinfo, mthod = environ['PATH_INFO'].rstrip('/'), environ['REQUEST_METHOD']
        for uexp, pobj in self.route:
            if uexp == pinfo:
                f = getattr(pobj, mthod, lambda e:'{} no method {}'.format(pinfo,mthod).encode())
                return f(environ) or b''
        return b'ERROR: dont match any route.'
def app(environ, start_response, router):
    rheaders = [('Content-type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'POST'),
                ('Access-Control-Allow-Headers', 'x-requested-with,content-type'),]
    start_response("200 OK", rheaders)
    return [router.parse(environ)]

# 按照以下模式增加 class 来处理各种接口请求
class parse_a:
    def GET(environ):
        query = environ['QUERY_STRING']
        # params = dict(parse_qsl(query)) # 将url参数解析成字典
        return query.encode()
class parse_b:
    def POST(environ):
        body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
        return body
router = Router([
    ('/a', parse_a),
    ('/b', parse_b),
])

def main():
    my_server = make_server('', 8000, lambda e,s:app(e,s,router), WS)
    my_server.serve_forever()

import threading
threading.Thread(target=main).start()


# 测试代码
import time
time.sleep(1)
from urllib import request
a = request.urlopen('http://127.0.0.1:8000/a?123=333')
b = request.urlopen('http://127.0.0.1:8000/b?123=333',data='asdfasdf'.encode())
print(a.read())
print(b.read())
