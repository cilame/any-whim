# _*_ coding:UTF-8 _*_  
import win32con
import ctypes
import ctypes.wintypes
import threading
import traceback
import tkinter
import os
import tempfile
from PIL import ImageGrab
user32 = ctypes.windll.user32

class HotkeyHooker:
    EXIT = False
    regdict = {}
    combins = set()
    tempids = list(range(1000))
    EXIT_ID = 1000

    def run(self):
        for tid in self.regdict:
            '''
            需要注意的是，注册函数需要和捕捉任务的线程一致，否则注册无效。
            '''
            if not user32.RegisterHotKey(None, tid, self.regdict[tid]['combine'], self.regdict[tid]['key']):
                print("rebind register id", self.regdict[tid]['key'])
                user32.UnregisterHotKey(None, self.regdict[tid]['key'])
        try:  
            msg = ctypes.wintypes.MSG()
            while True:
                for modkey in self.combins:
                    if user32.GetMessageA(ctypes.byref(msg), None, modkey, 0) != 0:
                        if msg.message == win32con.WM_HOTKEY:
                            if msg.wParam in self.regdict:
                                try:
                                    self.regdict[msg.wParam]['callback']()
                                except:
                                    traceback.print_exc()
                                if msg.wParam == self.EXIT_ID:
                                    return
                        user32.TranslateMessage(ctypes.byref(msg))
                        user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for key in self.regdict:
                user32.UnregisterHotKey(None, key)

    def start(self, ensure_exit=True):
        if ensure_exit:
            '''
            默认检测程序是否设计了程序退出的快捷键，没有则强制报错
            也可以简单配置 start 参数取消检测
            '''
            if self.EXIT_ID not in self.regdict:
                raise KeyError('exit callback not included, pls use "HotkeyHooker.regexit" func reg it.')
        threading.Thread(target=self.run).start()

    def reg(self, key, callback=lambda:None, combine=0):
        '''
        1, MOD_ALT
        2, MOD_CONTROL
        4, MOD_SHIFT
        8, MOD_WIN
        通过 | 运算进行组合，组合键处理一共有16种组合方式。
        例如 control+shift+win+alt+KEY 的组合键就需要combine填15

        这里为了语义更方便处理，combine也能通过字符串接收组合键需求
        可以直接将 combine 参数设置为 'control+shift' 也能实现组合键功能
        参数也可以不需要填入 '+' 符号，'controlshift' 这样的结果也是一样的
        为了语义更明确，建议输入时候带上 + 符号。

        
        另外 key 也能接收单个字符串，不过请注意，目前语义加深做得不够好
        目前只能接收字母作为组合键的 key，如果需要 F1 这类的键位
        请直接使用 win32con.VK_F10 直接作为 key 即可绑定。
        '''
        if type(combine) == str:
            _combine = 0
            _combine = _combine|1 if 'alt'      in combine.lower() else _combine
            _combine = _combine|2 if 'control'  in combine.lower() else _combine
            _combine = _combine|4 if 'shift'    in combine.lower() else _combine
            _combine = _combine|8 if 'win'      in combine.lower() else _combine
            combine = _combine

        if type(key) == str and len(key) == 1:
            key = ord(key.upper())

        self.combins.add(combine)
        self.regdict[self.tempids.pop()] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }

    def regexit(self, key, callback=lambda:None, combine=0):
        self.combins.add(combine)
        self.regdict[self.EXIT_ID] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }











# 处理一些实时回显以及处理 DEBUG 方面的功能
import win32gui, win32api
class MouseManager:
    def drawtext(self, text):
        '''
        在鼠标所在为止写入一个字符串
        '''
        t = win32gui.GetDC(win32gui.GetDesktopWindow())
        w,h = win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)
        x,y = win32api.GetCursorPos()
        win32gui.DrawText(t,text,-1,(x,y,w,h),8)

    def get_curr_pos(self):
        return win32api.GetCursorPos()

    def quick_clicks(self, pos:'Default CurrPos'=None):
        '''
        连点处理，没有坐标则直接使用鼠标当前为止坐标
        '''
        if pos:
            win32api.SetCursorPos(pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

click_toggle = False
def start_click():
    global click_toggle
    click_toggle = True
    def _():
        mm = MouseManager()
        while click_toggle:
            import time;time.sleep(.1)
            mm.quick_clicks()
    from threading import Thread
    Thread(target=_).start()

def stop_click():
    global click_toggle
    click_toggle = False











# 主要的截图处理工具，用于快速截图或者鼠标框选部分进行定位处理的工具
class PicCapture:
    def __init__(self, root, png):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.top = tkinter.Toplevel(root, width=sw, height=sh)
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=sw, height=sh)
        self.image  = tkinter.PhotoImage(file=png)
        self.canvas.create_image(sw//2, sh//2, image=self.image)
        self.fin_draw = None
        def btndown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            self.sel = True
        self.canvas.bind('<Button-1>', btndown)
        def btnmove(event):
            if not self.sel:
                return
            try:
                self.canvas.delete(self.fin_draw)
            except Exception as e:
                pass
            self.fin_draw = self.canvas.create_rectangle(
                                    self.X.get(), 
                                    self.Y.get(), 
                                    event.x, 
                                    event.y, 
                                    outline='red')
            
        self.canvas.bind('<B1-Motion>', btnmove)
        def btnup(event):
            self.sel = False
            try:
                self.canvas.delete(self.fin_draw)
            except Exception as e:
                pass
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            self.pic = ImageGrab.grab((left, top, right, bottom))
            self.rect = (left, top, right, bottom)
            self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', btnup)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

def screenshot_rect(root):
    filename = os.path.join(os.path.dirname(tempfile.mktemp()), 'temp.png')
    snapshot = ImageGrab.grab()
    snapshot.save(filename)
    snapshot.close()
    picshot = PicCapture(root, filename)
    root.wait_window(picshot.top)
    print(picshot.rect)
    # picshot.pic.show() # 简单展示图片
    os.remove(filename)







# 这部分主要就是 GUI 的处理，为了更加人性化的使用
# 后续会在该 GUI 主窗口中丰富主要的功能。
import tkinter
class KeyManagerGui():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", lambda:None)
        self.draw = True

    def exit(self):
        self.show_root() # 如果不显示就退出可能出现卡死错误。
        self.root.wm_attributes('-topmost',1)
        self.root.quit()

    def start(self):
        self.root.mainloop()


    def show_root(self):
        if not self.draw:
            self.root.deiconify() # 显示隐藏窗口。withdraw 和 deiconify 为配对的函数。
            self.draw = True

    def hide_root(self):
        if self.draw:
            self.root.withdraw()
            self.draw = False

    def switch_draw(self):
        print('F1')
        if self.draw:
            self.root.withdraw()
            self.draw = False
        else:
            self.root.deiconify() # 显示隐藏窗口。withdraw 和 deiconify 为配对的函数。
            self.draw = True







def test_log():
    print('test_log')








if __name__ == '__main__':
    keygui = KeyManagerGui()
    hotkey = HotkeyHooker()
    hotkey.regexit( win32con.VK_F4,  keygui.exit) # 将窗口关闭挂钩到热键里面
    hotkey.reg    ( win32con.VK_F1,  keygui.switch_draw)


    mouse = MouseManager()
    hotkey.reg    ( win32con.VK_F2,  lambda:mouse.drawtext(str(mouse.get_curr_pos())+'\n当前坐标'))
    hotkey.reg    ( win32con.VK_F3,  lambda:screenshot_rect(keygui.root))


    # 测试连点功能
    hotkey.reg    ( win32con.VK_F5,  start_click)
    hotkey.reg    ( win32con.VK_F6,  stop_click)


    # 测试能不能挂钩鼠标左键右键
    hotkey.reg    ( 1,  test_log)


    hotkey.start() # 注意 start 开启的顺序是 hotkey 兑现先挂钩再进入 keygui 的窗口循环事件当中
    keygui.start()
