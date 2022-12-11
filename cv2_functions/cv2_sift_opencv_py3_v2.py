# 需要安装一些库
# pip install opencv-contrib-python==3.4.1.15 
# 直接安装这个就可以了

import cv2
import numpy as np

# 从大图（22）中找到匹配小图（11）的部分，并进行大图（22）中的定位
i1 = cv2.imread('11.jpg')
i2 = cv2.imread('22.jpg')
DIS = 0.5 # 这个参数越小越严格，不要太大也不要太小
s = cv2.xfeatures2d.SIFT_create()
kp1,des1 = s.detectAndCompute(i1,None)
kp2,des2 = s.detectAndCompute(i2,None)
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)



# 调试显示特征点的代码，如果确定可以就删除下面这块代码保留功能代码即可
good = []
for m,n in matches:
    if m.distance <= DIS * n.distance:
        good.append([m])
i3 = cv2.drawMatchesKnn(i1,kp1,i2,kp2,good,None)
cv2.imshow('nier', i3)



# 功能代码，获取匹配特征点的重心进行处理
good = []
for m,n in matches:
    if m.distance < DIS * n.distance:
        good.append([m.trainIdx, m.queryIdx])
xx = yy = 0
for d1,d2 in good:
    x, y = kp2[d1].pt
    xx += int(x)
    yy += int(y)
xx = xx/len(good)
yy = yy/len(good)
print('centre of gravity in match point:',xx,yy)

# 在被定位的位置上画个圈圈
cv2.circle(i2, (int(xx), int(yy)), 3, (0, 0, 255), 5)
cv2.imshow('g', i2)

cv2.waitKey(0)
cv2.destroyAllWindows()