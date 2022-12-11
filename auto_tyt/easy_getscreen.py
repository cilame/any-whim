# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import ImageGrab
import ctypes

def get_screen():
    return np.asarray(ImageGrab.grab())

class RECT(ctypes.Structure):  
    _fields_ = [('left', ctypes.c_int),  
                ('top', ctypes.c_int),  
                ('right', ctypes.c_int),  
                ('bottom', ctypes.c_int)]  

def get_window_abs_by_name(name, show = False):
    screen = get_screen()
    rect = RECT()
    mhd = ctypes.windll.User32.FindWindowW(None,name)
    ctypes.windll.user32.GetWindowRect(mhd, ctypes.byref(rect))
    if rect.top == rect.bottom == rect.left == rect.right == 0:
        raise 'cant get windows'
    img = screen[rect.top:rect.bottom,rect.left:rect.right]
    b,g,r = map(lambda i:i[...,None],[img[...,0],img[...,1],img[...,2]])
    img = np.concatenate((r,g,b),axis=-1)
    if show:
        cv2.imshow('123',img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    return img

if __name__ == "__main__":
    get_window_abs_by_name('BlueStacks App Player', show=True)# win7 扫雷名
