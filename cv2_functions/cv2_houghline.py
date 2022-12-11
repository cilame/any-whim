import cv2
from numpy import *
v = cv2.imread('n.jpg')
#s = cv2.cvtColor(v,cv2.COLOR_BGR2GRAY)
v = cv2.resize(v,(v.shape[1]/2,v.shape[0]/2))

s = cv2.Canny(v,50,100)

t = cv2.HoughLinesP(s,1,pi/180,100,100,10)
for i in t:
    x1,y1,x2,y2 = i[0]
    cv2.line(v,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('nier1',s)
cv2.imshow('nier',v)
cv2.waitKey()
cv2.destroyAllWindows()
