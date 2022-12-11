# easyocr 安装和使用
# 该项目的识别率感觉和百度高精度的识别率差不多，而且可离线可无限使用！

# 模型可以从git项目里面找git的下载地址或者用下面的地址下载
# 链接：https://pan.baidu.com/s/1QzmMgOwIoCou_n2iDR1Q9A 
# 提取码：i6fl

# 1 先使用pip下载项目
# 	pip install easyocr
# 2 找到pytorch网页，按照官网给的方式下载，（注意选择是否需要gpu的版本）
# 3 如果在 import easyocr 时出现了错误：
#   Error loading "D:\Coding\Anaconda\lib\site-packages\torch\lib\asmjit.dll"
#   下载这个软件 https://aka.ms/vs/16/release/vc_redist.x64.exe 然后安装即可
#   如果该地址找不到软件，可以从上面的百度网盘里面找找看。
# 4 下载模型地址，可以在上面的百度网盘里面下载对应的模型
#   其中 craft_mlt_25k.pth 是必须的，其他语言按需下载即可。不过建议尽量全部都下载。
#   个人主要使用 latin 和 chinese_sim 这两个，下载后将文件都放到
#   用户路径下的 /.EasyOCR/model 文件路径下即可，
# 	如果还不知道这个路径在哪，请直接执行下面一行脚本输出的地址就是目标地址
#   import os;print(os.path.join(os.path.expanduser('~'),'.EasyOCR','model'))

import easyocr
reader = easyocr.Reader(['ch_sim','en'], gpu=False)
result = reader.readtext('1.png')
print(result)