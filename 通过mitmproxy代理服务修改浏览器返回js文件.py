# change_js.py
import re
import json
from mitmproxy.http import flow

def response(flow: flow):
    target_url = 'https://www.baidu.com'
    if  target_url in flow.request.url:
        jscode = flow.response.get_text()
        jscode = jscode.replace('debugger', '')
        flow.response.set_text(jscode)
        print('changed.', flow.request.url)

# 功能：使用 mitmproxy 修改浏览器请求返回的数据，用于绕过浏览器返回的js中的某些反调试js代码。
#     使用 fiddler 也能做到，不过那种修改起来比较麻烦
#     使用 mitmproxy 可以使用 python 代码来修改返回信息，对我来说会更加方便一些
#     这样可以更简单的实现更加复杂的替换操作
#
# 需要安装 mitmproxy： pip install mitmproxy -i https://pypi.douban.com/simple
# 使用该库的命令行工具 mitmdump 来创建一个代理端口
#
# mitmdump -q -s change_js.py -p 8888
# # -q 静音模式(仅限制该代码内的打印输出) -s 指定mitm中间件代码(即当前代码脚本) -p 指定端口(默认8080)
# 
# 使用代理方式打开 chrome ，建议使用 chromedriver 方式来增加代理打开，有时命令行打开代理无效
# --proxy-server=http://127.0.0.1:8888
# 下面的代码就是使用 chromedriver 打开使用代理的浏览器的代码
def get_driver():
    from selenium import webdriver
    option = webdriver.ChromeOptions()
    extset = ['enable-automation', 'ignore-certificate-errors']
    option.add_argument("--disable-infobars")                       # 关闭调试信息
    option.add_experimental_option("excludeSwitches", extset)       # 关闭调试信息
    option.add_experimental_option("useAutomationExtension", False) # 关闭调试信息
    option.add_argument('--proxy-server=http://127.0.0.1:8080')   # 代理端口修改就修改这里
    driver_path = 'chromedriver'
    webdriver = webdriver.Chrome(chrome_options=option, executable_path=driver_path)
    import threading, time
    def hook_close_window():
        chrome_close = False
        while not chrome_close:
            time.sleep(.3) # 每0.3秒检测一次
            driver_logs = webdriver.get_log('driver')
            for i in driver_logs:
                if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                    chrome_close = True
                    webdriver.quit()
                    print('webdriver is closed.')
    threading.Thread(target=hook_close_window).start()
    return webdriver
driver = get_driver()