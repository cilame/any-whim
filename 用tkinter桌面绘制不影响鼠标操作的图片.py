
import tkinter
import platform
import ctypes
if platform.architecture()[0] == "32bit":
    SetWindowLong = ctypes.windll.user32.SetWindowLongW
elif platform.architecture()[0] == "64bit":
    SetWindowLong = ctypes.windll.user32.SetWindowLongPtrW


# label = tkinter.Label(text='Powered by \nHogeHoge株式会社', font=('メイリオ','40'), fg='snow', bg='red')
# label.master.overrideredirect(True)
# window_width = 700
# window_height = 100
# label.master.geometry(str(window_width) + "x" + str(window_height) + "+400+300")
# label.master.lift()
# label.master.wm_attributes("-topmost", True)
# label.master.wm_attributes("-disabled", True)
# label.master.wm_attributes("-transparentcolor", "red")
# SetWindowLong(int(label.master.frame(), 16), -20, 168296488)
# def call_back_func():
#     print("call_back_funcの実行")
#     label.master.geometry(str(window_width) + "x" + str(window_height) + "+500+600")
#     label.master.lift()
#     label.after(1000, call_back_func)
#     # label.quit()
#     # label.destroy()
# label.pack()
# label.after(1000, call_back_func)
# label.mainloop()


# exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
# win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def get_mouse_point():
    po = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(po))
    return int(po.x), int(po.y)

canvas = tkinter.Canvas(bg='gray', highlightthickness=0, borderwidth=0)
canvas.create_rectangle(0,0,0+10,0+10)
canvas.master.lift()
canvas.master.wm_attributes("-topmost", True)
canvas.master.wm_attributes("-disabled", True)
canvas.master.wm_attributes("-alpha", 0.2)
canvas.master.wm_attributes("-fullscreen", True)
# canvas.master.overrideredirect(True)
# canvas.master.wm_attributes("-transparentcolor", "black")

canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
SetWindowLong(int(canvas.master.frame(), 16), -20, 168296488)
def call_back_func():
    # 这里要想办法获取所有窗口的信息，如果窗口信息有变化，就删除全部，重新绘制
    canvas.delete('all')

    x, y = get_mouse_point()
    x1,y1,x2,y2 = x,y,x+10,y+10
    canvas.create_rectangle(x1,y1,x2,y2,fill='black')

    x, y = get_mouse_point()
    x, y = x+20,y+20
    x1,y1,x2,y2 = x,y,x+10,y+10
    canvas.create_rectangle(x1,y1,x2,y2,fill='black')

    x, y = get_mouse_point()
    x, y = x-20,y-20
    x1,y1,x2,y2 = x,y,x+10,y+10
    canvas.create_rectangle(x1,y1,x2,y2,fill='black')

    x, y = get_mouse_point()
    x, y = x-20,y
    x1,y1,x2,y2 = x,y,x+10,y+10
    canvas.create_rectangle(x1,y1,x2,y2,fill='black')

    canvas.after(10, call_back_func)
canvas.after(10, call_back_func)
canvas.mainloop()