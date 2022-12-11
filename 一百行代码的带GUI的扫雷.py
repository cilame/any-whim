import random, sys, time
import numpy as np
def get_9(y,x):
    return np.maximum(y-1,0),y+2,np.maximum(x-1,0),x+2
def mine_1to8(y,x,mask,mine):mask[y,x] = mine[y,x]
def mine_zero(y,x,mask,mine,indx):
    sets,lists = set(),[(y,x)]
    while lists:
        y,x = lists.pop()
        if (y,x) not in sets:
            ly,ry,lx,rx = get_9(y,x)
            ax,bx = mine[ly:ry,lx:rx],indx[ly:ry,lx:rx]
            nexs = set(map(lambda i:tuple(i),bx[np.where(ax==0)]))
            lists += list(nexs)
        sets.add((y,x))
    for y,x in sets:
        ly,ry,lx,rx = get_9(y,x)
        mask[ly:ry,lx:rx] = mine[ly:ry,lx:rx]
def mine_init(h,w,minenum,iy,ix):
    v = np.random.sample((h*w,))
    v[np.argsort(v)[:minenum]] = -1
    v[v!=-1] = 0
    v = v.reshape((h,w)).astype(np.int32)
    zero,mine = list(zip(*np.where(v==0))),list(zip(*np.where(v!=0)))
    if (iy,ix) in mine: # first click must no mine
        change = random.choice(zero)
        mine.append(change),mine.remove((iy,ix))
        zero.remove(change),zero.append((iy,ix))
        v[change],v[(iy,ix)] = v[(iy,ix)],v[change]
    for y,x in zero:
        mx = v[np.maximum(y-1,0):y+2,np.maximum(x-1,0):x+2]
        v[y,x] = len(mx[mx==-1])
    mask = np.ones((h,w),dtype=np.int32) * -1
    indx = np.concatenate(tuple(map(lambda i:i[...,None], np.mgrid[:h,:w])),axis=-1)
    if v[iy,ix]==0: mine_zero(iy,ix,mask,v,indx)
    if v[iy,ix]!=0: mine_1to8(iy,ix,mask,v)
    return mask,indx,v
def flash(mask,k=True):
    temptime()
    global minenum,outcome
    for i,j in indx.reshape((-1,2)):
        if mask[i,j] != -1:
            if mask[i,j] != 0:
                exec("e%d_%d['text']=mask[%d,%d]"%(i,j,i,j))
            if k:exec("e%d_%d['relief']='groove'"%(i,j))
        elif not k:
            exec("e%d_%d['text']='X'"%(i,j))
    if len(mask[mask==-1])==varn.get() and outcome ==0:
        outcome = 1
        hwn.set('you win. ^_^')
def foo(i,j):
    if 'mask' not in globals():
        global mask,indx,mine,starttime,outcome
        starttime,outcome = time.time(),0
        mask,indx,mine = mine_init(varh.get(),varw.get(),varn.get(),i,j)
        flash(mask)
    elif outcome==0:
        temptime()
        if mine[i,j] != -1:
            if mine[i,j]==0:mine_zero(i,j,mask,mine,indx)
            if mine[i,j]!=0:mine_1to8(i,j,mask,mine)
            flash(mask)
        else:
            flash(mine,False)
            hwn.set('you fail. ToT')
def temptime():vartime.set('time cost: %3.2f | reset'%(time.time()-starttime))
def reset():
    global h,w,num
    if not (h == varh.get() and w ==varw.get() and num == varn.get()):
        globals()['minearea'].destroy()
        create_minearea(varh.get(),varw.get())
        globals()['minearea'].pack()
        h,w,num = varh.get(),varw.get(),varn.get()
    if 'mask' in globals():
        for i in range(varh.get()):
            for j in range(varw.get()):
                exec("e%d_%d['text']=''"%(i,j))
                exec("e%d_%d['relief']='flat'"%(i,j))
        globals().pop('mask'),hwn.set(" height    width    num     "),vartime.set('time cost: 0.00 | reset')
if sys.version[0] == '2':from Tkinter import *
if sys.version[0] == '3':from tkinter import *
master,timearea,inputarea,minearea,vartime = Tk(),Frame(),Frame(),Frame(),StringVar(value='time cost: 0.00 | reset')
master.resizable(width=False, height=False)
Button(timearea,width=20,textvariable=vartime,relief='groove',command=reset).pack(pady=3)
varh,varw,varn,hwn = IntVar(value=16),IntVar(value=18),IntVar(value=25),StringVar(value=" height    width    num     ")
Label(inputarea,width=20,textvariable=hwn,relief='groove').grid(columnspan=3,sticky=W+E+N+S,padx=3,pady=3)
Entry(inputarea,width=6,textvariable=varh,relief='ridge').grid(row=1,column=0,padx=3,pady=3)
Entry(inputarea,width=6,textvariable=varw,relief='ridge').grid(row=1,column=1,padx=3,pady=3)
Entry(inputarea,width=6,textvariable=varn,relief='ridge').grid(row=1,column=2,padx=3,pady=3)
def create_minearea(h,w):
    globals()['minearea'] = Frame()
    for i in range(h):
        for j in range(w):
            exec('def func%d_%d():foo(%d,%d)'%(i,j,i,j))
            exec("globals()['e%d_%d'] = Button(minearea,text='',width=2,relief='flat',command=func%d_%d)"%(i,j,i,j))
            exec("globals()['e%d_%d'].grid(row=i,column=j,sticky=W+E+N+S)"%(i,j))
create_minearea(varh.get(),varw.get())
h,w,num = varh.get(),varw.get(),varn.get()
master.title('minimine'),timearea.pack(),inputarea.pack(),minearea.pack()
mainloop()
