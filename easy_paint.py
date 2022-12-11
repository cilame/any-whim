import cv2
import numpy as np

def drawMouse(event,x,y,flags,param):
    color = (0,0,0)
    global xx,yy
    if flags == cv2.EVENT_FLAG_LBUTTON:
        cv2.line(img,(xx,yy),(x,y),color,5)
    xx,yy = x,y

img = np.ones((300,300,3))*255
cv2.imshow('img',img)
cv2.setMouseCallback('img',drawMouse)

print 's means save, c means close, space means clear.'
while True:
    key = cv2.waitKey(10)
    cv2.imshow('img',img)
    if key == ord(' '):
        img = np.ones((300,300,3))*255
    if key == ord('s'):
        cv2.imwrite('output.jpg',img)
    if key == ord('c'):
        break

cv2.destroyAllWindows()
