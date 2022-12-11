import cv2

s = cv2.createBackgroundSubtractorMOG2(varThreshold=100)
f = cv2.VideoCapture(0)

while(1):
    a,v = f.read()
    g = s.apply(v)
    g = cv2.morphologyEx(g,cv2.MORPH_DILATE,(7,7),iterations=7)

    a,b,c = cv2.findContours(g,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in b:
        x,y,w,h = cv2.boundingRect(i)
        if w>10 and h>10:cv2.rectangle(v,(x,y),(x+w,y+h),(0,255,0),1)

    cv2.imshow('nier1',v)
    cv2.imshow('nier',g)
    if cv2.waitKey(42)==ord(' '):
        break

f.release()
cv2.destroyAllWindows()
