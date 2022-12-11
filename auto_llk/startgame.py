import cv2, random, time
from llk import *
from easy_getscreen import *
from grid_spliter import *
from keras.models import load_model
from CreateCate import CreateCate

import win32api,win32con

def cat_val2num(cates2class):
    ids = list(range(1,len(cates2class)))
    for idx,value in cates2class.items():
        if value!='0':
            cates2class[idx] = ids.pop()
        else:
            cates2class[idx] = 0

print('loading models...')
modeler = load_model('mytrain_model.h5')
cater = CreateCate()
cates2class = cater.load_mapdict('mycate_model.pickle')
cat_val2num(cates2class)
print('loading models ok.')

def get_pred_s_map(grider,modeler,cater,cates2class):
    s_map = np.zeros((gridh,gridw))
    for i in range(gridh):
        for j in range(gridw):
            pic = grider.get_picmat_by_point(i,j)[None,]
            pr = modeler.predict(pic.astype(np.float32)/255.)
            cls = cater.get_class_by_cate(cates2class,pr)
            s_map[i,j] = cls
    return s_map

def l2a(p,grider,top=0,left=0):
    a,b,c,d = grider.lr_shape[p[0],p[1]]
    return int((b+d)/2+left), int((a+c)/2+top)

def click(p):
    win32api.SetCursorPos(p)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

gridh,gridw = 11,19

def run(window_name,leave=0,log=True,save_temp=True,human=True,speed_gap=0.):
    v = get_window_abs_by_name(window_name)[181:566,14:603]
    if save_temp:
        cv2.imwrite('temp.png',v)
    grider = GridSpliter(v,gridh,gridw)
    s_map = get_pred_s_map(grider,modeler,cater,cates2class).astype(np.int32)
    chain = get_chain(s_map)
    top,left = get_window_top_left(window_name)
    top,left = top+181,left+14
    if leave==0:
        leave=-10000000
    lenchain = len(chain)
    for a,b in chain[:-leave]:
        if log:
            print(lenchain)
        lenchain -= 1
        ################ make click like a human
        if human:
            if random.random()<.5 and lenchain>40:
                time.sleep(0.8-speed_gap+random.random()*.8)
            elif random.random()<.4 and lenchain>30 and lenchain<=40:
                time.sleep(0.8-speed_gap+random.random()*.7)
            elif random.random()<.3 and lenchain>20 and lenchain<=30:
                time.sleep(0.8-speed_gap+random.random()*.6)
            elif random.random()<.2 and lenchain>10 and lenchain<=20:
                time.sleep(0.8-speed_gap+random.random()*.5)
            else:
                time.sleep(0.7-speed_gap+random.random()*.4)
        #######################
        pa,pb = l2a(a,grider,top,left),l2a(b,grider,top,left)
        click(pa)
        click(pb)


window_name = 'QQ游戏 - 连连看角色版'
##run(window_name)
