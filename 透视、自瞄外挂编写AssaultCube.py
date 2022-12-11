# 学习透视相关的内容
# 尝试写一个 AssaultCube 游戏的透视、自瞄外挂以便测试结果

# 开发环境 win10 python3.6
# 只能在局域网透视别人，目前没调试出 bot 的追踪。
# 由于用的画框的函数性能问题，追个一两个人还行，追踪太多人的轨迹可能还是有点卡。
# 自瞄需要依赖 pip install pynput

import math
import struct
from ctypes import *
from ctypes.wintypes import *

def get_all_pids_names():
    ret = []
    lpidProcess = (c_ulong * 256)()
    cb          = sizeof(lpidProcess)
    cbNeeded    = c_ulong()
    hModule     = c_ulong()
    count       = c_ulong()
    modname     = c_buffer(30)
    flag        = 0x0010 | 0x0400 # PROCESS_VM_READ|PROCESS_QUERY_INFORMATION
    windll.psapi.EnumProcesses(byref(lpidProcess), cb, byref(cbNeeded))
    pidProcess = [i for i in lpidProcess][:int(cbNeeded.value/sizeof(c_ulong()))]
    for pid in pidProcess:
        hProcess = windll.kernel32.OpenProcess(flag, False, pid)
        if hProcess:
            windll.psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            windll.psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            ret.append((pid, b"".join([ i for i in modname if i != b'\x00'])))
            for i in range(modname._length_):
                modname[i] = b'\x00'
            windll.kernel32.CloseHandle(hProcess)
    return ret
def get_pid_from_name(name):
    pids_names = get_all_pids_names()
    name = name.encode() if isinstance(name,str) else name
    for pid, _name in pids_names:
        if name == _name:
            return pid

# 通过进程名获取进程的句柄
def get_process_handle(pid):
    return windll.kernel32.OpenProcess(0x1f0fff, False, pid)

def read_buffer(hProcess, lpBaseAddress, nSize):
    lpBuffer = create_string_buffer(nSize)
    result = windll.kernel32.ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, 0)
    if result is None or result == 0:
        raise Exception('Error: %s' % GetLastError())
    return lpBuffer.raw

def byte_to_float(bytes):
    return struct.unpack('<f', struct.pack('4B', *bytes))[0]

def read_matrix(handle, addr):
    ret = []
    for g in range(16):
        if g % 4 == 0: ret.append([])
        bt = read_buffer(handle, addr+(g*4), 4)
        ret[-1].append(byte_to_float(bt))
    return ret

def read_list_float(handle, addr, num):
    ret = []
    for g in range(num):
        bt = read_buffer(handle, addr+(g*4), 4)
        ret.append(byte_to_float(bt))
    return ret

def byte_to_int(bytes):
    return struct.unpack('<i', struct.pack('4B', *bytes))[0]

def read_list_int(handle, addr, num):
    ret = []
    for g in range(num):
        bt = read_buffer(handle, addr+(g*4), 4)
        ret.append(byte_to_int(bt))
    return ret

def read_addr(handle, addr):
    bt = read_buffer(handle, addr, 4)
    return int(''.join(['{:02x}'.format(i) for i in bt][::-1]), 16)

def write_float(handle, addr, num):
    fnum = c_float(num)
    windll.kernel32.WriteProcessMemory(handle, addr, byref(fnum), sizeof(c_float), 0)

# 在窗口画一个矩形
windc = None
def draw_rect(x1,y1,x2,y2):
    global windc
    if not windc: windc = windll.user32.GetDC(0)
    r = RECT(x1,y1,x2,y2)
    windll.user32.FrameRect(windc, byref(r), windll.gdi32.GetStockObject(0))

# 通过进程名获取该进程的窗口句柄
def get_window_size(handle):
    rect = RECT()
    try: # win10 的处理方式
        windll.dwmapi.DwmGetWindowAttribute(HWND(handle),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect) )
    except:
        windll.user32.GetWindowRect(handle, byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom

# 通过进程名获取进程的窗口句柄
def get_window_handle(pid):
    top = ctypes.windll.user32.GetTopWindow(None)
    handle = HWND()
    while top:
        hd = windll.user32.GetWindowThreadProcessId(top, byref(handle))
        if hd != 0 and pid == handle.value:
            if not windll.user32.GetParent(top) and windll.user32.IsWindowVisible(top):
                return top
        top = windll.user32.GetWindow(top, 2) # GW_HWNDNEXT

def read_value(hProcess, lpBaseAddress, nSize):
    lpBuffer = create_string_buffer(nSize)
    result = windll.kernel32.ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, 0)
    if result is None or result == 0:
        raise Exception('Error: %s' % GetLastError())
    return lpBuffer

def read_addr_byplist(handle, start_addr, offset_list=None):
    v = read_addr(handle, start_addr)
    if offset_list:
        for offset in offset_list:
            v = read_addr(handle, v + offset)
    return v

def get_enemies_infos(handle, num=16):
    # 获取其他玩家的坐标地址，需要从CE中调试出来
    ret = []
    for i in range(1,num+1):
        try:
            v = read_addr_byplist(handle, 0x0050F4F8, offset_list=[4*i])
            r = read_list_float(handle, v+0x34, 3)
            hp = read_list_int(handle, v+0xF8, 1)[0]
            isEnemy = read_list_int(handle, v+0x32C, 1)[0]
            ret.append([r, hp, isEnemy])
        except:
            pass
    return ret

class BITMAPINFOHEADER(Structure):
    _fields_ = [('biSize', DWORD), ('biWidth', LONG), ('biHeight', LONG),
                ('biPlanes', WORD), ('biBitCount', WORD),
                ('biCompression', DWORD), ('biSizeImage', DWORD),
                ('biXPelsPerMeter', LONG), ('biYPelsPerMeter', LONG),
                ('biClrUsed', DWORD), ('biClrImportant', DWORD)]
class BITMAPINFO(Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', DWORD * 3)]
class BLENDFUNCTION(Structure):
    _fields_ = [('BlendOp', BYTE),
                ('BlendFlags', BYTE),
                ('SourceConstantAlpha', BYTE),
                ('AlphaFormat', BYTE)]
class draw_transparent_rect:
    bf = BLENDFUNCTION()
    bf.BlendOp = 0
    bf.BlendFlags = 0
    bf.SourceConstantAlpha = 100 #//透明程度//值越大越不透明
    bf.AlphaFormat = 0
    srcdc = windll.user32.GetDC(0)
    rects = {}
    def __init__(self):
        super().__init__()
    def draw_rect(self, rect):
        x1,y1,x2,y2 = rect
        width = x2 - x1
        height = y2 - y1
        if rect not in self.rects:
            bflen = height * width * 3
            image = create_string_buffer(bflen)
            srcdc = windll.user32.GetDC(0)
            memdc = windll.gdi32.CreateCompatibleDC(srcdc)
            bmp = windll.gdi32.CreateCompatibleBitmap(memdc, width, height)
            windll.gdi32.SelectObject(memdc, bmp)
            self.rects[rect] = {}
            self.rects[rect]['memdc'] = memdc
        memdc = self.rects[rect]['memdc']
        rect = byref(RECT(1,1,width-1,height-1))
        windll.user32.FrameRect(memdc, rect, windll.gdi32.GetStockObject(0))
        windll.msimg32.AlphaBlend(self.srcdc, x1,y1,width,height, memdc, 0, 0, width, height, self.bf)

def get_myinfo():
    myangle_addr_x = read_addr_byplist(handle, 0x00509B74) + 0x40
    myangle_addr_y = read_addr_byplist(handle, 0x00509B74) + 0x44
    myhp = read_list_int(handle, myangle_addr_x+0xB8, 1)[0]
    myside = read_list_int(handle, myangle_addr_x+0x2ec, 1)[0]
    return (myangle_addr_x, myangle_addr_y), myhp, myside

def get_myaddr_xy():
    my_addr = read_addr_byplist(handle, 0x00509B74) + 0x34
    my_addr = read_list_float(handle, my_addr, 3)
    return my_addr

def get_dis(myaddr, enemyaddr):
    return ((enemyaddr[1] - myaddr[1])**2 + (enemyaddr[0] - myaddr[0])**2)**.5

def get_newangle(enemy_addr):
    my_addr = get_myaddr_xy()
    xangle = math.atan2((enemy_addr[1] - my_addr[1]), (enemy_addr[0] - my_addr[0])) * (180/math.pi)
    yangle = math.atan2((enemy_addr[2] - my_addr[2]), get_dis(my_addr, enemy_addr)) * (180/math.pi)
    return 90 + xangle, yangle-.5

def focus_enemy(enemy_addr):
    if enemy_addr:
        (myangle_addr_x, myangle_addr_y), myhp, myside = get_myinfo()
        newangle_x, newangle_y = get_newangle(enemy_addr)
        write_float(handle, myangle_addr_x, newangle_x)
        write_float(handle, myangle_addr_y, newangle_y)

focus_toggle = False
def focus_nearest_enemy(nearest_enemy):
    focus_enemy(nearest_enemy)

def draw_enemies_rect(handle, whandle, num=16):
    global focus_toggle
    M = read_matrix(handle, 0x00501AE8) # 自己矩阵信息，即摄像机信息，需要从CE中调试出来
    # Px, Py, Pz = [73.10000610351562, 118.89999389648438, -4] # 目标的世界坐标
    myaddr, myhp, myside = get_myinfo()
    my_addr_xy = get_myaddr_xy()
    length = float('inf')
    count = 0
    head = 4 
    feet = -.5
    dlist = {}
    for (Px, Py, Pz), hp, isEnemy in get_enemies_infos(handle, num):
        if myside != isEnemy and myhp > 0 and myhp <= 100 and hp > 0 and hp <= 100:
            count += 1
            G = windll.user32.GetSystemMetrics
            if windll.user32.IsZoomed(whandle):
                L, T, R, B, H = 0, 0, G(0), G(1), 0
            else:
                (L, T, R, B), H = get_window_size(whandle), 0#G(4)
            Gx = int((R-L)/2)
            Gy = int((B-T)/2)
            VieW = Px * M[0][3] + Py * M[1][3] + Pz * M[2][3] + M[3][3]
            VieW = 1 / VieW
            Bx  = Gx + (Px * M[0][0] + Py * M[1][0] + Pz * M[2][0] + M[3][0]) * VieW * Gx
            By  = Gy - (Px * M[0][1] + Py * M[1][1] + (Pz+head) * M[2][1] + M[3][1]) * VieW * Gy
            By2 = Gy - (Px * M[0][1] + Py * M[1][1] + (Pz+feet) * M[2][1] + M[3][1]) * VieW * Gy
            wid = abs(By - By2)*.23
            x1, y1, x2, y2 = int(Bx-wid), int(By), int(Bx+wid), int(By2)
            x1, y1, x2, y2 = x1+int(L), y1+int(T)+H, x2+int(L), y2+int(T)+H
            _length = get_dis(my_addr_xy, (Px, Py))
            dlist[_length] = (x1, y1, x2, y2), (Px, Py, Pz)
    if count:
        if dlist:
            (x1, y1, x2, y2), (Px, Py, Pz) = dlist[min(dlist)] 
            # 只显示最近的一个人的框，效果实际上不太好，如果能选择距离鼠标最近的一个，那估计会好很多
            # (x1, y1, x2, y2) 为屏幕的坐标，那么也就是说，获取当前坐标位置来处理判断也会很方便
            # 后续再考虑改改看。
            draw_rect(x1, y1, x2, y2)
            if focus_toggle and count:
                focus_nearest_enemy((Px, Py, Pz))

def on_click(x,y,button,key):
    global focus_toggle
    if button.name == 'right':
        focus_toggle = key

def hook_mouse_right_key():
    try:
        from pynput import mouse
        mlisten = mouse.Listener(on_click=on_click)
        mlisten.start()
    except Exception as e:
        print('无法加载鼠标右键挂钩')
        print(e)

process_name = 'ac_client.exe' # 注意这里是进程名字，不是窗口名字
pid = get_pid_from_name(process_name)
print('process id:{}'.format(pid))
handle  = get_process_handle(pid)
whandle = get_window_handle(pid)
drect = draw_transparent_rect()

def run(num=16):
    print('启动外挂')
    hook_mouse_right_key()
    while 1:
        draw_enemies_rect(handle, whandle, num)
        # import time
        # time.sleep(.01)

run(16) # python 性能不行，尽量不要画太多的框。








# 原始的绘制透明
# height = 200
# width = 100
# bmi = BITMAPINFO()
# bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER)
# bmi.bmiHeader.biWidth = width
# bmi.bmiHeader.biHeight = -height  # Why minus? See [1]
# bmi.bmiHeader.biPlanes = 1
# bmi.bmiHeader.biBitCount = 24
# bmi.bmiHeader.biCompression = BI_RGB
# class BLENDFUNCTION(Structure):
#     _fields_ = [('BlendOp', BYTE),
#                 ('BlendFlags', BYTE),
#                 ('SourceConstantAlpha', BYTE),
#                 ('AlphaFormat', BYTE)]
# bf = BLENDFUNCTION()
# bf.BlendOp = 0
# bf.BlendFlags = 0
# bf.SourceConstantAlpha = 0x3f #//透明程度//值越大越不透明
# bf.AlphaFormat = 0
# bflen = height * width * 3
# image = create_string_buffer(bflen)
# srcdc = windll.user32.GetDC(0)
# memdc = windll.gdi32.CreateCompatibleDC(srcdc)
# bmp = windll.gdi32.CreateCompatibleBitmap(memdc, width, height)
# windll.gdi32.SelectObject(memdc, bmp)
# rect = byref(RECT(1,1,width-1,height-1))
# windll.user32.FrameRect(memdc, rect, windll.gdi32.GetStockObject(0))
# windll.msimg32.AlphaBlend(srcdc, 0, 0, width, height, memdc, 0, 0, width, height, bf)