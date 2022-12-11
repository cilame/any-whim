# -*- coding: utf-8 -*-
from easy_getscreen import get_window_abs_by_name

import cv2
import numpy as np

import win32api,win32con
import time, math


# 用的是蓝叠模拟器
# 这些数值是根据当前模拟器窗口为 432x768 运算所得
# 而因为是通过截屏取窗口，所以运算时使用的长宽会稍微大一些
#h = 573
#w = 444
key = 281.85

# 鼠标按压时间
def pushtime(t):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
    time.sleep(t)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

# 获取自身的坐标
def get_my_point(s,t):
    h,w = t.shape[:2]
    v = cv2.matchTemplate(s,t,cv2.TM_CCOEFF)
    a,b,c,d = cv2.minMaxLoc(v)
    top_left = d
    bot_right = d[0]+w,d[1]+h
    my_point = int(d[0]+w/2),int(d[1]+h-w/4)
    cv2.line(s,my_point,my_point,(0,0,0),3)
    cv2.rectangle(s,top_left, bot_right, (0,0,0), 2)
    return my_point

# 获取下一步的坐标
def get_top_point(s,my_point):
    h = 573
    w = 444
    x = 30
    xita = x/180.
    xita = math.tan(math.pi*xita)
    y = int(h - w * xita)
    o_h,o_w = s.shape[:2]
    top_gap = 250
    gap = 16
    v = s[top_gap:,gap:o_w-gap*2]
    center_w = int(v.shape[1]/2)
    if my_point[0]<o_w/2:
        s = v[:,center_w:v.shape[1]]
        s = np.argmax(s,axis=0)
        k = np.argmin(s[12:])
        k = s[k]
        temp = np.where(s==k)[0]
        k = (temp.max()+temp.min())/2
        top_w = int(k+center_w+gap)
        top_y = int((y-h)/w*top_w + h) #(0,h),(w,y)
        return top_w,top_y
    else:
        s = v[:,0:center_w]
        s = np.argmax(s,axis=0)
        k = np.argmin(s[:-12])
        k = s[k]
        temp = np.where(s==k)[0]
        k = (temp.max()+temp.min())/2
        top_w = int(k+gap)
        top_y = int((y-h)/(-w)*(top_w-w) + (h-10)) #(w,h-10),(0,y-10)
        return top_w,top_y

# 对当前坐标进行修正以获取距离
def get_right_dst(s,my_point,top_point):
    h = 573
    w = 444
    x = 30
    xita = x/180.
    xita = math.tan(math.pi*xita)
    y = int(h - w * xita)
    o_h,o_w = s.shape[:2]
    #(0,h),   (w,y)
    #(0,y-10),(w,h-10)
    # 这里需要注意，后面坐标系转换成了一般数学常用坐标系
    # 因为后面只用计算距离了，就不再转换回来麻烦了
    mx,my = my_point
    if mx<o_w/2:
        k = math.tan(-math.pi/6)
        my = h - my
        x_,y_ = 0,0
    else:
        k = math.tan(math.pi/6)
        my = h - my
        x_,y_ = 0,w * xita

    #(y-my)/(x-mx) = k
    #(y-y_)/(x-x_) = -k
    #find x,y
    y = ((x_-mx)*k+(my+y_))/2
    x = (mx+x_)/2 + (y_-my)/(2*k)
    tx,ty = top_point
    ty = h - ty
    return ((x-tx)**2+(y-ty)**2)**.5

# 开始
def run():
    while 1:
        time.sleep(2.5)
        o = get_window_abs_by_name('BlueStacks App Player')
        s = o.copy()
        t = cv2.imread('templ.bmp')
        my_point = get_my_point(s,t)
        s = cv2.Canny(s,70,120)
        top_point = get_top_point(s,my_point)
        dst = get_right_dst(s,my_point,top_point)
        pushtime(dst/key)

time.sleep(3)
run()

##o = get_window_abs_by_name('BlueStacks App Player')
##s = o.copy()
##t = cv2.imread('templ.bmp')
##my_point = get_my_point(s,t)
##s = cv2.Canny(s,70,120)
##top_point = get_top_point(s,my_point)
##dst = get_right_dst(s,my_point,top_point)
##print(my_point)
##print(top_point)
##print(dst)
##cv2.line(o,top_point,top_point,(0,0,0),5)
##cv2.line(o,my_point,my_point,(0,0,0),5)
##cv2.imshow('123',o)
##cv2.imshow('456',s)
##cv2.waitKey()
##cv2.destroyAllWindows()
