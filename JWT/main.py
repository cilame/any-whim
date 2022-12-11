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
            if not user32.RegisterHotKey(None, tid, self.regdict[tid]['combine'], self.regdict[tid]['key']):
                print("rebind register id", self.regdict[tid]['key'])
                user32.UnregisterHotKey(None, self.regdict[tid]['key'])
        try:  
            msg = ctypes.wintypes.MSG()  
            while True:
                for modkey in self.combins:
                    if user32.GetMessageA(ctypes.byref(msg), None, modkey, 0) != 0:
                        if msg.message == 786: # win32con.WM_HOTKEY
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
            if self.EXIT_ID not in self.regdict:
                raise KeyError('exit callback not included, pls use "HotkeyHooker.regexit" func reg it.')
        threading.Thread(target=self.run).start()
    def parse_combine(self, combine):
        if type(combine) == str:
            _combine = 0
            _combine = _combine|1 if 'alt'      in combine.lower() else _combine
            _combine = _combine|2 if 'control'  in combine.lower() else _combine
            _combine = _combine|4 if 'shift'    in combine.lower() else _combine
            _combine = _combine|8 if 'win'      in combine.lower() else _combine
            combine = _combine
        return combine
    def reg(self, key, combine=0, callback=lambda:None):
        if type(key) == str and len(key) == 1:
            key = ord(key.upper())
        combine = self.parse_combine(combine)
        self.combins.add(combine)
        self.regdict[self.tempids.pop()] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }
    def regexit(self, key, combine=0, callback=lambda:None):
        combine = self.parse_combine(combine)
        self.combins.add(combine)
        self.regdict[self.EXIT_ID] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }














# 遍历当前页面所有窗口的窗口名字
def enumerate_all_window_names():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles

# 通过名字获取窗口的 numpy 类型的图片数据
import cv2
import numpy as np
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND

GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC
def get_window_behind_by_name(name, x1x2y1y2=None):
    handle = ctypes.windll.User32.FindWindowW(None,name)
    windll.user32.SetProcessDPIAware()
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    npimg = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
    b,g,r = map(lambda i:i[...,None],[npimg[...,0],npimg[...,1],npimg[...,2]])
    npimg = np.concatenate((b,g,r),axis=-1)
    if x1x2y1y2:
        x1, x2, y1, y2 = x1x2y1y2
        npimg = npimg[x1:x2, y1:y2]
    def test():
        cv2.imshow('123',npimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # test()
    return npimg

















import ctypes
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW
MAPVK_VK_TO_VSC = 0
INTERCEPTION_KEY_DOWN = 0x00
INTERCEPTION_KEY_UP = 0x01
INTERCEPTION_MOUSE_MOVE_ABSOLUTE = 0x001
INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN = 0x001
INTERCEPTION_MOUSE_LEFT_BUTTON_UP = 0x002
INTERCEPTION_KEYBOARD = lambda index: ((index) + 1)
INTERCEPTION_MOUSE = lambda index: (10 + (index) + 1)
interception = ctypes.CDLL('./interception_64.dll')
interception.interception_create_context.restype = ctypes.POINTER(ctypes.c_void_p)
class InterceptionMouseStroke(ctypes.Structure):
    _fields_ = [('state',       ctypes.c_ushort),
                ('flags',       ctypes.c_ushort),
                ('rolling',     ctypes.c_short),
                ('x',           ctypes.c_int),
                ('y',           ctypes.c_int),
                ('information', ctypes.c_uint)]
class InterceptionKeyStroke(ctypes.Structure):
    _fields_ = [('code',        ctypes.c_ushort),
                ('state',       ctypes.c_ushort),
                ('information', ctypes.c_uint)]
VkCode = {
    "back": 0x08,      "snapshot": 0x2C,  "separator": 0x6C, "end": 0x23,       "numpad5": 0x65,   "f7": 0x76,
    "tab": 0x09,       "insert": 0x2D,    "subtract": 0x6D,  "home": 0x24,      "numpad6": 0x66,   "f8": 0x77,
    "return": 0x0D,    "delete": 0x2E,    "decimal": 0x6E,   "left": 0x25,      "numpad7": 0x67,   "f9": 0x78,
    "shift": 0x10,     "lwin": 0x5B,      "divide": 0x6F,    "up": 0x26,        "numpad8": 0x68,   "f10": 0x79,
    "control": 0x11,   "rwin": 0x5C,      "f1": 0x70,        "right": 0x27,     "numpad9": 0x69,   "f11": 0x7A,
    "menu": 0x12,      "numpad0": 0x60,   "f2": 0x71,        "down": 0x28,      "multiply": 0x6A,  "f12": 0x7B,
    "pause": 0x13,     "numpad1": 0x61,   "f3": 0x72,        "print": 0x2A,     "add": 0x6B,       "numlock": 0x90,
    "capital": 0x14,   "numpad2": 0x62,   "f4": 0x73,        "scroll": 0x91,    "lshift": 0xA0,    "rshift": 0xA1,
    "escape": 0x1B,    "numpad3": 0x63,   "f5": 0x74,        "lcontrol": 0xA2,  "rcontrol": 0xA3,  "lmenu": 0xA4,
    "space": 0x20,     "numpad4": 0x64,   "f6": 0x75,        "rmenu": 0XA5
}
import time
import string
VkKeyScanA = ctypes.windll.user32.VkKeyScanA
def get_virtual_keycode(key: str):
    return (VkKeyScanA(ord(key)) & 0xff) if len(key) == 1 and key in string.printable else VkCode[key]

def keyboard_click(key):
    key = get_virtual_keycode(key)
    time.sleep(0.009)
    context = interception.interception_create_context()
    keyStroke = (InterceptionKeyStroke * 1)()
    keyStroke[0].code = MapVirtualKey(key, MAPVK_VK_TO_VSC)
    keyStroke[0].state = INTERCEPTION_KEY_DOWN
    interception.interception_send(context, 1, keyStroke, keyStroke._length_)
    time.sleep(0.017)
    context = interception.interception_create_context()
    keyStroke = (InterceptionKeyStroke * 1)()
    keyStroke[0].code = MapVirtualKey(key, MAPVK_VK_TO_VSC)
    keyStroke[0].state = INTERCEPTION_KEY_UP
    interception.interception_send(context, INTERCEPTION_KEYBOARD(0), keyStroke, keyStroke._length_)
    interception.interception_destroy_context(context)

desktop_w = ctypes.windll.user32.GetSystemMetrics(0)
desktop_h = ctypes.windll.user32.GetSystemMetrics(1)
def mouse_left_click(x, y):
    context = interception.interception_create_context()
    mouseStroke = (InterceptionMouseStroke * 3)()
    mouseStroke[0].flags = INTERCEPTION_MOUSE_MOVE_ABSOLUTE
    mouseStroke[0].x = int(65535 * x / desktop_w)
    mouseStroke[0].y = int(65535 * y / desktop_h)
    mouseStroke[1].state = INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    mouseStroke[2].state = INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    interception.interception_send(context, INTERCEPTION_MOUSE(0), mouseStroke, mouseStroke._length_)
    interception.interception_destroy_context(context)

def mouse_set_pos(x, y):
    context = interception.interception_create_context()
    mouseStroke = (InterceptionMouseStroke * 1)()
    mouseStroke[0].flags = INTERCEPTION_MOUSE_MOVE_ABSOLUTE
    mouseStroke[0].x = int(65535 * x / desktop_w)
    mouseStroke[0].y = int(65535 * y / desktop_h)
    interception.interception_send(context, INTERCEPTION_MOUSE(0), mouseStroke, mouseStroke._length_)
    interception.interception_destroy_context(context)




 











def get_match(exp, titles):
    import re
    rets = []
    for title in titles:
        if re.findall(exp, title):
            rets.append(title)
    return rets

def get_jwt_window_bg(name):
    return get_window_behind_by_name(name, [530, 530+65, 150, 150+750])

def get_jwt_window_bar(name):
    return get_window_behind_by_name(name, [510, 510+23, 505, 505+180])


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), 
                ("y", ctypes.c_long)]
def get_mouse_pos():
    pos = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
    return [pos.x, pos.y]
def set_mouse_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

class RECT(ctypes.Structure):  
    _fields_ = [('left', ctypes.c_int),  
                ('top', ctypes.c_int),  
                ('right', ctypes.c_int),  
                ('bottom', ctypes.c_int)]  
def get_window_rect(name):
    rect = RECT()
    mhd = ctypes.windll.User32.FindWindowW(None, name)
    ctypes.windll.user32.GetWindowRect(mhd, ctypes.byref(rect))
    return [rect.left, rect.top, rect.right, rect.bottom]

def findmatchtemplate_np_muti(front_np, bg_np, match_threshold=0.94, nms_threshold=0.5):
    def pre_deal(v, left=180, right=240):
        # v = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
        # v = cv2.Canny(v, left, right)
        return v
    bg_np = cv2.pyrMeanShiftFiltering(bg_np, 5, 50)
    img1 = pre_deal(front_np)
    img2 = pre_deal(bg_np)
    w, h = img1.shape[:2]
    v = cv2.matchTemplate(img2,img1,cv2.TM_CCORR_NORMED)
    index = np.where(v > match_threshold)
    infos = []
    for idx, i in enumerate(zip(*index[::-1])):
        xy1xy2 = [i[0], i[1], i[0]+w, i[1]+h]
        infos.append(xy1xy2)
    def nms(infos):
        if not infos: return infos
        def iou(xyxyA,xyxyB):
            ax1,ay1,ax2,ay2 = xyxyA
            bx1,by1,bx2,by2 = xyxyB
            minx, miny = max(ax1,bx1), max(ay1, by1)
            maxx, maxy = min(ax2,bx2), min(ay2, by2)
            intw, inth = max(maxx-minx, 0), max(maxy-miny, 0)
            areaA = (ax2-ax1)*(ay2-ay1)
            areaB = (bx2-bx1)*(by2-by1)
            areaI = intw*inth
            return areaI/(areaA+areaB-areaI)
        rets = []
        infos = infos[::-1]
        while infos:
            curr = infos.pop()
            if rets and any([iou(r, curr) > nms_threshold for r in rets]):
                continue
            rets.append(curr)
        return rets
    infos = nms(infos)
    def test():
        timg = img2.copy()
        for x1, y1, x2, y2 in infos:
            timg = cv2.rectangle(timg, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.imshow('nier', timg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # test()
    return infos

class JWT:
    def __init__(self, name, bpm):
        self.bpm = bpm
        self.np_bar_sign = cv2.imread('./imgs/bar_sign.png')

        self.np_up = cv2.imread('./imgs/up.png')
        self.np_down = cv2.imread('./imgs/down.png')
        self.np_left = cv2.imread('./imgs/left.png')
        self.np_right = cv2.imread('./imgs/right.png')
        self.np_l_up = cv2.imread('./imgs/l_up.png')
        self.np_l_down = cv2.imread('./imgs/l_down.png')
        self.np_r_up = cv2.imread('./imgs/r_up.png')
        self.np_r_down = cv2.imread('./imgs/r_down.png')
        self.np_red_up = cv2.imread('./imgs/red_up.png')
        self.np_red_down = cv2.imread('./imgs/red_down.png')
        self.np_red_left = cv2.imread('./imgs/red_left.png')
        self.np_red_right = cv2.imread('./imgs/red_right.png')
        self.np_red_l_up = cv2.imread('./imgs/red_l_up.png')
        self.np_red_l_down = cv2.imread('./imgs/red_l_down.png')
        self.np_red_r_up = cv2.imread('./imgs/red_r_up.png')
        self.np_red_r_down = cv2.imread('./imgs/red_r_down.png')
        v = 3
        self.np_up = self.np_up[v:-v, v:-v, ]
        self.np_down = self.np_down[v:-v, v:-v, ]
        self.np_left = self.np_left[v:-v, v:-v, ]
        self.np_right = self.np_right[v:-v, v:-v, ]
        self.np_l_up = self.np_l_up[v:-v, v:-v, ]
        self.np_l_down = self.np_l_down[v:-v, v:-v, ]
        self.np_r_up = self.np_r_up[v:-v, v:-v, ]
        self.np_r_down = self.np_r_down[v:-v, v:-v, ]
        self.np_red_up = self.np_red_up[v:-v, v:-v, ]
        self.np_red_down = self.np_red_down[v:-v, v:-v, ]
        self.np_red_left = self.np_red_left[v:-v, v:-v, ]
        self.np_red_right = self.np_red_right[v:-v, v:-v, ]
        self.np_red_l_up = self.np_red_l_up[v:-v, v:-v, ]
        self.np_red_l_down = self.np_red_l_down[v:-v, v:-v, ]
        self.np_red_r_up = self.np_red_r_up[v:-v, v:-v, ]
        self.np_red_r_down = self.np_red_r_down[v:-v, v:-v, ]

        titles = get_match(name, enumerate_all_window_names())
        if not titles:
            raise Exception('没有找到窗口')
        self.window_name = titles[0]

    def get_side(self, np_side, np_bg, name):
        ret = []
        for i in findmatchtemplate_np_muti(np_side, np_bg):
            ret.append([name, i])
        return ret

    def get_process(self):
        cost = time.time()
        np_bar = get_jwt_window_bar(self.window_name)
        sign = findmatchtemplate_np_muti(self.np_bar_sign, np_bar)
        if sign:
            bar_len = np_bar.shape[1] - 22
            bar_sig = sign[0][0]
            return bar_sig / bar_len, time.time() - cost

    def focus_window(self):
        pos = get_mouse_pos()
        rect = get_window_rect(self.window_name)
        mouse_left_click(rect[0]+100, rect[1]+100)
        time.sleep(0.1)
        mouse_set_pos(pos[0], pos[1])

    def get_list(self):
        # 目前识别存在很小几率识别错误。
        np_bg = get_jwt_window_bg(self.window_name)
        v_list = []
        v_list.extend(self.get_side(self.np_up, np_bg, 'up'))
        v_list.extend(self.get_side(self.np_down, np_bg, 'down'))
        v_list.extend(self.get_side(self.np_left, np_bg, 'left'))
        v_list.extend(self.get_side(self.np_right, np_bg, 'right'))
        v_list.extend(self.get_side(self.np_l_up, np_bg, 'l_up'))
        v_list.extend(self.get_side(self.np_l_down, np_bg, 'l_down'))
        v_list.extend(self.get_side(self.np_r_up, np_bg, 'r_up'))
        v_list.extend(self.get_side(self.np_r_down, np_bg, 'r_down'))

        v_list.extend(self.get_side(self.np_red_up, np_bg, 'red_up'))
        v_list.extend(self.get_side(self.np_red_down, np_bg, 'red_down'))
        v_list.extend(self.get_side(self.np_red_left, np_bg, 'red_left'))
        v_list.extend(self.get_side(self.np_red_right, np_bg, 'red_right'))
        v_list.extend(self.get_side(self.np_red_l_up, np_bg, 'red_l_up'))
        v_list.extend(self.get_side(self.np_red_l_down, np_bg, 'red_l_down'))
        v_list.extend(self.get_side(self.np_red_r_up, np_bg, 'red_r_up'))
        v_list.extend(self.get_side(self.np_red_r_down, np_bg, 'red_r_down'))

        v_list = sorted(v_list, key=lambda a:a[1][0])
        v_list = [i[0] for i in v_list]
        return v_list

    def get_mapkey_name(self, kname):
        kmap = {
            'up': 'numpad8',
            'down': 'numpad2',
            'left': 'numpad4',
            'right': 'numpad6',
            'l_up': 'numpad7',
            'l_down': 'numpad1',
            'r_up': 'numpad9',
            'r_down': 'numpad3',
            'red_up': 'numpad2',
            'red_down': 'numpad8',
            'red_left': 'numpad6',
            'red_right': 'numpad4',
            'red_l_up': 'numpad3',
            'red_l_down': 'numpad9',
            'red_r_up': 'numpad1',
            'red_r_down': 'numpad7',
        }
        return kmap[kname]

    def calc_time(self, process, bpm, cost):
        proc = 0.71 - process
        proc = 0 if proc < 0 else proc
        proc = proc * 60 / bpm * 4 - cost
        return 0 if proc < 0 else proc

    def run(self, s_list):
        print(s_list)
        if not s_list:
            return
        self.focus_window()
        for key in s_list:
            keyboard_click(self.get_mapkey_name(key))
        proc_cost = self.get_process()
        if not proc_cost:
            return
        process, cost = proc_cost
        wtime = self.calc_time(process, self.bpm, cost)
        print(wtime)
        time.sleep(wtime)
        keyboard_click('space')
        time.sleep(60 / self.bpm * 4 * 1.01)

# jwt = JWT('劲舞团[^区]+区', 155)
# jwt.run(jwt.get_list())
# jwt.run(jwt.get_list())
# jwt.run(jwt.get_list())
# jwt.run(jwt.get_list())
# jwt.run(jwt.get_list())

# 后面得优化一下识别率，识别率真的很低。

import threading
toggle = {'x': True}
def run_main():
    jwt = JWT('劲舞团[^区]+区', 202)
    while toggle['x']:
        jwt.run(jwt.get_list())
threading.Thread(target=run_main).start()
def close():
    toggle['x'] = False

hotkey = HotkeyHooker()
hotkey.regexit(112, 'alt', close) # alt F1 关闭
hotkey.start()

# titles = get_match('劲舞团[^区]+区', enumerate_all_window_names())
# get_jwt_window_bar(titles[0])


