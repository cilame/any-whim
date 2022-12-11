# filename:setup.py
from setuptools import setup

# 为了让你写的 python 工具能够通过 pip 进行下载
# 你可以使用下面的方式对你的工具进行打包

# 使用pypi作为你的工具库的前提有两个
# 1 你得有一个 pypi 的账号，并且用户路径配置了 .pypirc
#   [ 用户路径通常情况会是右边的这个 ]: C:\Users\Administrator
#   不过有时你不是管理员用户的话，（快捷键win+r后输入cmd时弹出的默认路径）
#   那么 Administrator 这个名字就应该变成你进入电脑的账号
#   并且这个 .pypirc 文件（文件前面带.符号可能在windows下不能直接生成）
#   用py脚本 open(".pypirc","w") 生成一个这个名字的文件即可
#   然后用文本编辑器编辑该文件内容成下面的样子：
#       [distutils]
#       index-servers=pypi
#       [pypi]
#       repository = https://upload.pypi.org/legacy/
#       username = 这里写你的明文账号
#       password = 这里写你的明文密码
# 2 这个工具库的名字没有被别人占用
#   直接用 pip search 来搜索一个库是否有被别人占用
#   或者直接从 pypi 的官网上去搜索，没有该名字你就能直接使用
 
setup(
    
    # ==== 必要参数就这两个 ====
    # 其他参数甚至不填都能进行上传
    # 注意同一 version 版本不能 upload 两次
    # 在该脚本下执行下面的命令行指令（该命令需预先安装 wheel 库，pip install wheel 即可）：
    # python setup.py bdist_wheel upload
    # 
    # 现在旧版的 upload 出现问题，用 twine 上传避免bug（需要 pip 下载）
    # pip install twine
    # twine upload dist/*
    name = "vv",
    version = "0.0.7",
    

    # ==== 用于描述该库信息的参数 ====
    keywords = "vv",#大概是用于被pypi搜索的一些关键词
    author = "placeholder", #作者名字
    author_email = "placeholder@placeholder.com",#作者联系邮件
    url="https://placeholder",#该库的开源地址
    license = "MIT",#开源协议
    description = "placeholder.",#显示在 pip search 中的简短描述
    long_description = 'placeholder.',#显示在pypi函数页中的长描述
    long_description_content_type="text/markdown",
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    

    # ==== 用于配置前置需求的参数 ====
    packages = ["cc"], # 开发库的名字，setup路径下需要包含的包
    #python_requires=">=3.6", # 版本需求
    #install_requires=[
    #    'vv', # 依赖库
    #],


    # ==== 用于配置命令行工具的使用方式的参数 ====
    # 配置后会在 python 的 script 包内生成一个vv的命令行工具
    # 只要有配置 python 的环境变量的话，那在任意路径下就能直接使用
    # vv 命令行工具，非常非常方便的接口
    entry_points={
        'console_scripts': ['vv = cc.xx:execute']
    },
)
