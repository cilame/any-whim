
# 使用时需要预先安装 interception 的驱动
# 需要在管理员模式下的 cmd 命令行里面执行： install-interception.exe /install
# (直接双击运行没用的，卸载驱动为：install-interception.exe /uninstall)

import ctypes
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW
MAPVK_VK_TO_VSC = 0
INTERCEPTION_KEY_DOWN = 0x00
INTERCEPTION_KEY_UP = 0x01

INTERCEPTION_MOUSE_MOVE_RELATIVE = 0x000
INTERCEPTION_MOUSE_MOVE_ABSOLUTE = 0x001
INTERCEPTION_MOUSE_VIRTUAL_DESKTOP = 0x002
INTERCEPTION_MOUSE_ATTRIBUTES_CHANGED = 0x004
INTERCEPTION_MOUSE_MOVE_NOCOALESCE = 0x008
INTERCEPTION_MOUSE_TERMSRV_SRC_SHADOW = 0x100
INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN = 0x001
INTERCEPTION_MOUSE_LEFT_BUTTON_UP = 0x002
INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN = 0x004
INTERCEPTION_MOUSE_RIGHT_BUTTON_UP = 0x008
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
    time.sleep(0.03)
    context = interception.interception_create_context()
    keyStroke = (InterceptionKeyStroke * 1)()
    keyStroke[0].code = MapVirtualKey(key, MAPVK_VK_TO_VSC)
    keyStroke[0].state = INTERCEPTION_KEY_DOWN
    interception.interception_send(context, 1, keyStroke, keyStroke._length_)
    time.sleep(0.03)
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






import time
time.sleep(2)

keyboard_click('up')
mouse(100,200)


# cx = ctypes.windll.user32.GetSystemMetrics(0);
# cy = ctypes.windll.user32.GetSystemMetrics(1);
# print(cx, cy)