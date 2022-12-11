# 需要安装一些库
# pip install opencv-contrib-python==3.4.1.15 
# 直接安装这个就可以了

import cv2
import numpy as np

i1 = cv2.imread('11.jpg')
i2 = cv2.imread('22.jpg')

s = cv2.xfeatures2d.SIFT_create()
kp1,des1 = s.detectAndCompute(i1,None)
kp2,des2 = s.detectAndCompute(i2,None)

# 普通暴力匹配
# bf = cv2.BFMatcher(crossCheck=True)
# matches = bf.match(des1, des2)
# matches = sorted(matches, key=lambda i:i.distance)
# i3 = cv2.drawMatches(i1,kp1,i2,kp2,matches[:10],None)
# cv2.imshow('nier', i3)

# k对最佳匹配
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
good = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])
i3 = cv2.drawMatchesKnn(i1,kp1,i2,kp2,good,None)
cv2.imshow('nier', i3)



# 从大图（22）中找到匹配小图（11）的部分，并进行一定形变后直接展示图片
i1 = cv2.imread('11.jpg')
i2 = cv2.imread('22.jpg')

s = cv2.xfeatures2d.SIFT_create()
kp1,des1 = s.detectAndCompute(i1,None)
kp2,des2 = s.detectAndCompute(i2,None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
good = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m.trainIdx, m.queryIdx])

if len(good) > 4:
    pts1 = np.float32([kp1[i].pt for _,i in good])
    pts2 = np.float32([kp2[i].pt for i,_ in good])
    H, status = cv2.findHomography(pts2, pts1, cv2.RANSAC, 4.0)
    if H is None:
        print('error')
        exit()
    import pprint; pprint.pprint(H.tolist())
    result = cv2.warpPerspective(i2, H, i1.shape[:2][::-1])

cv2.imshow('j1', result)
cv2.waitKey(0)
cv2.destroyAllWindows()