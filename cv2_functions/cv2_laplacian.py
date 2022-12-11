import cv2

s = cv2.imread('nier2.jpg')
#s = cv2.morphologyEx(s,cv2.MORPH_OPEN,None,iterations=1)
#s = cv2.Canny(s,50,150)
s = cv2.erode(s,(3,3),iterations=3)
s = cv2.dilate(s,(3,3),iterations=3)
#s = cv2.blur(s,(5,5))
#s = cv2.GaussianBlur(s,(3,3),0)
s = cv2.cvtColor(s,cv2.COLOR_BGR2GRAY)
s = cv2.Laplacian(s,cv2.CV_16S,ksize=3)
s = cv2.convertScaleAbs(s)

cv2.imshow('niert',s)
ret, binary = cv2.threshold(s,40,255,cv2.THRESH_BINARY)
ins, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if w>5 and h>10:
        cv2.rectangle(s,(x,y),(x+w,y+h),(155,155,155),3)

#cv2.drawContours(s,contours,-1,(0,0,255),3)
cv2.imshow('binary',binary)
cv2.imshow('nier',s)
cv2.waitKey()
cv2.destroyAllWindows()
