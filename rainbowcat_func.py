import random,time,math
import win32gui,win32api
import mp3play
from win32con import *
t = win32gui.GetDC(win32gui.GetDesktopWindow())
w,h = win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)

s = [
    IDI_ERROR,
    IDI_WARNING,
    IDI_APPLICATION,
    IDI_EXCLAMATION,
    IDI_ASTERISK,
    IDI_HAND,
    IDI_INFORMATION,
    IDI_QUESTION,
    IDI_WINLOGO
    ]

def drawtext(times):
    tim = time.time()
    x,y = random.randint(0,w),random.randint(0,h)
    while time.time()-tim<times:
        time.sleep(.001)
        r = 60
        xx,yy = map(int,[random.gauss(0,r)+x,random.gauss(0,r)+y])
        win32gui.DrawText(t,'nihaoa',-1,(xx,yy,w,h),DT_BOTTOM)

def tennel(times):
    win32gui.StretchBlt(t,50,50,w-100,h-100,t,0,0,w,h,SRCCOPY)
    time.sleep(times)

def inversecolor():
    win32gui.BitBlt(t,0,0,w,h,t,0,0,NOTSRCCOPY)


def drawerror(times):
    tim = time.time()
    while time.time()-tim<times:
        time.sleep(.1)
        x,y = random.randint(0,w),random.randint(0,h)
        win32gui.DrawIcon(t,x,y,win32gui.LoadIcon(None,random.choice(s)))

try:
    music = mp3play.load('Running_In_The_90s.mp3')
    music.play()
except:
    pass
#------------
drawerror(12.5)
inversecolor()
for i in range(12):
    if i==6:inversecolor()
    drawtext(.5)
inversecolor()
for i in [1.3,1,.6,.4,.4,.4,.4,.3,.3]:
    tennel(i)
#------------
i = 1
while True:
    x,y = random.randint(0,w),random.randint(0,h)
    if (i+1)% 100==0:win32gui.DrawIcon(t,x,y,win32gui.LoadIcon(None,random.choice(s)))
    pi = math.pi
    parts = pi/10000
    lens = 15
    px,py = map(int,[math.cos(parts*i)*lens,math.sin(parts*i)*lens])
    if (i+1)%100==0:win32gui.StretchBlt(t,30+px,30+py,w-60+px,h-60+py,t,0,0,w,h,SRCCOPY)
    i+=1

