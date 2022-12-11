# 发送按键指令给窗口
from ctypes import windll
from ctypes.wintypes import HWND
import string
import time
PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
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
def get_virtual_keycode(key: str):
    return (VkKeyScanA(ord(key)) & 0xff) if len(key) == 1 and key in string.printable else VkCode[key]
def key_down(handle, key: str):
    if type(handle) == str: handle = ctypes.windll.User32.FindWindowW(None,handle)
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
def key_up(handle, key: str):
    if type(handle) == str: handle = ctypes.windll.User32.FindWindowW(None,handle)
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)

















import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW
MAPVK_VK_TO_VSC = 0
PUL = ctypes.POINTER(ctypes.c_ulong)
VkCodeList = {
    "back": 0x08,      "snapshot": 0x2C,  "separator": 0x6C, "end": 0x23,       "numpad5": 0x65,   "f7": 0x76,
    "tab": 0x09,       "insert": 0x2D,    "subtract": 0x6D,  "home": 0x24,      "numpad6": 0x66,   "f8": 0x77,
    "return": 0x0D,    "delete": 0x2E,    "decimal": 0x6E,   "numpad7": 0x67,   "f9": 0x78,        "left": MapVirtualKey(0x25, MAPVK_VK_TO_VSC),
    "shift": 0x10,     "lwin": 0x5B,      "divide": 0x6F,    "numpad8": 0x68,   "f10": 0x79,       "up": MapVirtualKey(0x26, MAPVK_VK_TO_VSC),
    "control": 0x11,   "rwin": 0x5C,      "f1": 0x70,        "numpad9": 0x69,   "f11": 0x7A,       "right": MapVirtualKey(0x27, MAPVK_VK_TO_VSC),
    "menu": 0x12,      "numpad0": 0x60,   "f2": 0x71,        "multiply": 0x6A,  "f12": 0x7B,       "down": MapVirtualKey(0x28, MAPVK_VK_TO_VSC),
    "pause": 0x13,     "numpad1": 0x61,   "f3": 0x72,        "print": 0x2A,     "add": 0x6B,       "numlock": 0x90,
    "capital": 0x14,   "numpad2": 0x62,   "f4": 0x73,        "scroll": 0x91,    "lshift": 0xA0,    "rshift": 0xA1,
    "escape": 0x1B,    "numpad3": 0x63,   "f5": 0x74,        "lcontrol": 0xA2,  "rcontrol": 0xA3,  "lmenu": 0xA4,
    "space": 0x20,     "numpad4": 0x64,   "f6": 0x75,        "rmenu": 0XA5
}
def get_vkcode(key: str):
    return (VkKeyScanA(ord(key)) & 0xff) if len(key) == 1 and key in string.printable else VkCodeList[key]
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def down_up(key, times=0.5):
    code = get_vkcode(key)
    PressKey(code)
    import time
    time.sleep(times)
    ReleaseKey(code)