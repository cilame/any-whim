# _*_ coding:UTF-8 _*_  
import win32con
import ctypes
import ctypes.wintypes
import threading
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
                                self.regdict[msg.wParam]['callback']()
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



if __name__ == '__main__':
    hotkey = HotkeyHooker()  
    hotkey.regexit(win32con.VK_F10)                      # F10   关闭
    hotkey.reg('a', lambda:print('asdfasdfasdf'), 'alt') # alt+a 调试函数输出
    hotkey.start()
