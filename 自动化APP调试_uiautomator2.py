# 使用 uiautomator2 作为调试工具
# pip install uiautomator2 -i https://pypi.douban.com/simple/
import uiautomator2 as ui

# 在安装了 adb 后，直接用 adb connect 目标模拟器/USB调试端口后
# 直接用如下方式即可连接
device = ui.connect()

# 【APP启动，包名查询】
# 直接使用APP显示的名字即可点击打开指定APP
# 获取当前打开的APP信息（可以获取包名）
# device(text='新浪新闻').click()
# curr = device.app_current()
# print(curr)
# device.app_start('com.sina.news') # 使用包名打开APP
# device.app_stop('com.sina.news')  # 使用包名关闭APP
# device.app_clear('com.sina.news') # 清除APP产生的临时文件

# 【设备信息】
# info = device.info
# dnfo = device.device_info
# size = device.window_size()
# # device.push
# # device.pull
# from pprint import pprint
# pprint(info) # 设备信息
# pprint(dnfo) # 设备详细信息
# pprint(size) # 窗口大小

# 【操作指令】
# device.screen_off()   # 熄屏
# device.screen_on()    # 亮屏
# device.press('power') # 有点类似于亮屏和熄频
# device.press('home')
# device.press('back')
# device.press('left')
# device.press('right')
# device.press('down')
# device.press('up')
# device.press('center')
# device.press('menu')
# device.press('search')
# device.press('enter')
# device.press('delete')
# device.press('recent')
# device.press('camera')

# 【气泡提示】
# 气泡提示数据展示和收集
# 不过这里的 show 似乎不能被 get_message 收集到
# device.toast.show("hello world.", 15)
# device.toast.get_message(3)







# 调试时使用 weditor 会比较方便的调试出 APP 内的数据信息
# 用于快速定位数据以及快速生成调试代码。
# 安装后在命令行直接使用 weditor 命令打开自动会打开一个网页，可以实时调试app。
# pip install weditor -i https://pypi.douban.com/simple/