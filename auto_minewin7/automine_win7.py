import cv2
from PIL import ImageGrab
import numpy as np
import win32gui,win32api,win32con
import random, os, time

def get_screen():
    return np.asarray(ImageGrab.grab())

def get_mine_pic(screen):
    mhd = win32gui.FindWindow('MineSweeper',None)
    x,y,w,h = win32gui.GetWindowRect(mhd)
    img = screen[y:h,x:w]
    b,g,r = map(lambda i:i[...,None],[img[...,0],img[...,1],img[...,2]])
    img = np.concatenate((r,g,b),axis=-1)
    lx,ly,rx,ry = 39,81,-37,-40
    h,w = img.shape[:2]
    img = img[ly:h+ry,lx:w+rx]
    return img

def get_pix_by_one(x,y,minepic):
    s = minepic[x*18:(x+1)*18,y*18:(y+1)*18]
    return s

def create_index(minepic):
    h,w = minepic.shape[:2]
    a,b = np.mgrid[:h/18,:w/18]
    v = np.concatenate((a[...,None],b[...,None]),-1)
    v = v.reshape((-1,2))
    return v

def get_num_hw(minepic):
    return map(lambda i:i/18,minepic.shape[:2])

def create_xywh(minepic):
    v = create_index(minepic)
    return np.hstack((v*18, (v+1)*18))

def create_sample(minepic):
    v = create_xywh(minepic)
    a,b = minepic.shape[:2]
    num = a*b/18/18
    temp = np.zeros((num,18,18,3))
    for index,(y,x,yw,xh) in enumerate(v):
        temp[index] = minepic[y:yw,x:xh]
    return temp

def setforegroundwindow():
    mhd = win32gui.FindWindow('MineSweeper',None)
    win32gui.SetForegroundWindow(mhd)

def random_name():
    return '%07d.png'%random.randint(0,999999)

def get_abs_mine_area():
    mhd = win32gui.FindWindow('MineSweeper',None)
    x,y,w,h = win32gui.GetWindowRect(mhd)
    px,py = 39,81
    absh,absw = py+y,px+x
    minepic = get_mine_pic(get_screen())
    h,w = minepic.shape[:2]
    hs,ws = np.mgrid[:h/18,:w/18]
    hs,ws = hs*18+absh+9,ws*18+absw+9
    v = np.concatenate((hs[...,None],ws[...,None]),-1)
    return v


if os.path.isfile('mycate_model.pickle') and os.path.isfile('mytrain_model.h5'):
    from CreateCate import CreateCate
    from keras.models import load_model
    s = CreateCate()
    catemodel = s.load_mapdict('mycate_model.pickle')
    model = load_model('mytrain_model.h5')
else:
    print 'file mytrain_model.h5 or mycate_model.pickle not find.'

def predict_map(minepic):
    v = create_sample(minepic)
    v = v.astype(np.float32)/255.
    pr = map(lambda i:s.get_class_by_cate(catemodel, i),model.predict(v))
    pr = np.array(pr).reshape(get_num_hw(minepic)).astype(np.int32)
    return pr

def predict_map_now():
    screen = get_screen()
    minepic = get_mine_pic(screen)
    return predict_map(minepic)


def find_mine_by_point(point,predict_map):
    maxh,maxw = predict_map.shape[:2]
    y,x = point
    lh = y-1 if y-1>0 else 0
    lw = x-1 if x-1>0 else 0
    rh = y+2 if y+2<maxh else maxh
    rw = x+2 if x+2<maxw else maxw
    minenum = predict_map[y,x]
    v = predict_map[lh:rh,lw:rw]
    if len(v[(v==-1)|(v==9)]) == minenum:
        v[v==-1] = 9

def find_mine_point(predict_map):
    for i in range(1,9):
        for j in np.array(np.where(predict_map==i)).transpose():
            find_mine_by_point(j,predict_map)

def find_safe_by_point(point,predict_map):
    maxh,maxw = predict_map.shape[:2]
    y,x = point
    lh = y-1 if y-1>0 else 0
    lw = x-1 if x-1>0 else 0
    rh = y+2 if y+2<maxh else maxh
    rw = x+2 if x+2<maxw else maxw
    minenum = predict_map[y,x]
    v = predict_map[lh:rh,lw:rw]
    if len(v[v==9]) == minenum:
        v[v==-1] = 10

def find_safe_point(predict_map):
    for i in range(1,9):
        for j in np.array(np.where(predict_map==i)).transpose():
            find_safe_by_point(j,predict_map)


def safe_predict_map():
    predict_map = predict_map_now()
    find_mine_point(predict_map)
    find_safe_point(predict_map)
    return predict_map

def get_safe_points(predict_map,abspoint_map):
    return abspoint_map[predict_map==10]

def click(point):
    win32api.SetCursorPos(point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

FOCUS = False
def find_mine_and_click_safe(abspoint_map,sleeptime):
    t = safe_predict_map()
    if len(t[t==10])==0:
        print 'cant find abs mine. time sleep 1s.'
        time.sleep(1)
        return
    global FOCUS
    for index,i in enumerate(get_safe_points(t,abspoint_map)):
        if not FOCUS:
            click(i[::-1])
            FOCUS = True
        click(i[::-1])
        time.sleep(sleeptime)

def start(stime=.03):
    abspoint_map = get_abs_mine_area()
    while True:
        find_mine_and_click_safe(abspoint_map,stime)


if __name__=='__main__':
    
    try:
        stime = float(input('pls input click ones need time(default:0.03):'))
        print 'input time:',stime
        start(stime)
    except:
        print 'default time: 0.03.'
        start()
    

