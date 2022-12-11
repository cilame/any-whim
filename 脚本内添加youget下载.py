
# 获取信息
import json
import builtins
import threading
import you_get.common
from you_get.common import url_to_module
from you_get.common import any_download
you_get.common.skip_existing_file_size_check = True # 跳过存在检查

gt = threading.RLock()
def download_video_limit_size(url, output_dir='.', minsize=0, maxsize=float('inf')): # 限制视频大小方便处理
    def get_info_from_url(url): # 这里的挂钩不适用于多线程
        m, url = url_to_module(url)
        jdata = None
        _org_print = print
        def _new_print(*a,**k):
            nonlocal jdata
            try: jdata = json.loads(a[0])
            except: pass
        builtins.print = _new_print
        m.download(url, merge=True, output_dir='.', info_only=False)
        builtins.print = _org_print
        return jdata
    with gt:
        you_get.common.json_output = True # 开启仅显示json文件
        info = get_info_from_url(url)
        size = info['streams']['__default__']['size'] / (2**20) # 使用的单位是M(兆)
        if size and size > minsize and size < maxsize:
            you_get.common.json_output = False # 关闭仅显示json文件
            any_download(url, output_dir=output_dir, merge=True, info_only=False)
            return info

url = 'http://vd3.bdstatic.com/mda-jiryepehgmwgari8/sc/mda-jiryepehgmwgari8.mp4'
info = download_video_limit_size(url, 'asdf你好')
print(info)

# 使用 pyinstaller 打包的时候需要额外添加如下命令行内容
# --add-data "e:\python\python36\Lib\site-packages\you_get;you_get" --add-data "e:\python\python36\Lib\xml;xml" --add-data "e:\python\python36\Lib\html;html" --add-binary "e:\python\python36\Lib\_markupbase.py;."
# 其中上面的全部 e:\python\python36 改成 python.exe 所在的地址即可，
# 如果不知道请使用 import os, sys; print(os.path.dirname(sys.executable)) 查看
# *由于不同的扩展可能需要的库不太一样，暂时没有调整打包出现的问题，后续再调整好了。





