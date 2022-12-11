import cv2

v = cv2.imread('pic.jpg')
#s = cv2.morphologyEx(s,cv2.MORPH_OPEN,None,iterations=1)
#s = cv2.Canny(s,50,150)
s = cv2.erode(v,(3,3),iterations=3)
s = cv2.dilate(s,(3,3),iterations=3)
#s = cv2.blur(s,(5,5))
#s = cv2.GaussianBlur(s,(3,3),0)
s = cv2.cvtColor(s,cv2.COLOR_BGR2GRAY)
s = cv2.Canny(s,70,140)
cv2.imshow('nier',s)
ret, binary = cv2.threshold(s,127,255,cv2.THRESH_BINARY)
ins, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if w>5 and h>10:
        cv2.rectangle(v,(x,y),(x+w,y+h),(155,155,0),1)

#cv2.drawContours(s,contours,-1,(0,0,255),3) 
cv2.imshow('nier',v)
cv2.waitKey()
cv2.destroyAllWindows()
