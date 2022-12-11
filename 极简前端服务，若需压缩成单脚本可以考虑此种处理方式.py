# 快速将打包成字符串的zip文件部署成可被线程执行的服务，
# 主要是为了更加方便的部署，一个脚本就能将前后端分离的前端部署上去
# 另外这里是可以以线程执行的，所以如果你有想法，甚至可以将后端也写在这个脚本里面，
# 这样可以快速实现一个脚本就能实现完整的前后端服务。
#
# 这里的zstring为一个txt文件的打包，解压后就是一个文件，'.' 代表的时相对地址，
# 如果解压后是一个文件夹，文件夹内的数据才是前端数据，那么就需要修改下面的 innerpath 为文件夹名字即可。
zstring = (
'3-D%U5n*6p;9%HY!V&mH?9qB|Fb{%DQj1IUN-9cr*Cf7v?A`D8o{=HIn~_PL0hbmP1_)4q'
'(l7(KpdyS65)5if_Z0c%USovOGdLc8_65=b-mGj8HH-{VK-v(j0{{'
)
innerpath = '.'

# len(zstring): 123
import base64, zlib
zstring = base64.b85decode(zstring)
zstring = zlib.decompress(zstring,-15)
bitdata = zstring

import os
import tempfile
zfilename = 'zfile.zip'
zsuffix = '_vilame_unzip'
tpath = tempfile.mkdtemp(suffix=zsuffix)
zfile = os.path.join(tpath, zfilename)
with open(zfile, 'wb') as f:
    f.write(bitdata)

import shutil
_tpath,_tname = os.path.split(tpath)
for _path in os.listdir(_tpath):
    cpath = os.path.join(_tpath, _path)
    if cpath.endswith(zsuffix) and _tname not in cpath:
        try: shutil.rmtree(cpath); print('remove cache: {}'.format(cpath))
        except: pass # if this failed. may reboot computer will be ok.

import zipfile
with zipfile.ZipFile(zfile) as zip_ref:
    zip_ref.extractall(zfile.replace(".zip",""))

import sys
import http.server
def myserver(protocol="HTTP/1.0", port=8000, bind=""):
    HandlerClass = http.server.SimpleHTTPRequestHandler
    ServerClass = http.server.HTTPServer
    server_address = (bind, port)
    HandlerClass.protocol_version = protocol
    with ServerClass(server_address, HandlerClass) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

inner = os.path.join(zfile.replace(".zip",""), innerpath) # 进入解压文件夹内的地址
os.chdir(inner)
print('work place: {}'.format(inner))
import threading
threading.Thread(target=myserver).start()