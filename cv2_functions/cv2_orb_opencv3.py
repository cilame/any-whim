import cv2  
import numpy as np
from matplotlib import pyplot as plt
  
img1 = cv2.imread('1.jpg')  
img2 = cv2.imread('2.jpg')  
  

orb = cv2.ORB_create(100)    
kp1, des1 = orb.detectAndCompute(img1,None)  
kp2, des2 = orb.detectAndCompute(img2,None)  

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

if len(matches)>10:

    src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches,None)
    plt.imshow(img3)
    plt.show()

    H,_ = cv2.findHomography(dst_pts,src_pts,cv2.RANSAC,5.0)
    wrap = cv2.warpPerspective(img2, H, (img2.shape[1]+img2.shape[1] , img2.shape[0]+img2.shape[0]))
    rows, cols = np.where(wrap[:,:,0] > 10)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    result = wrap[min_row:max_row,min_col:max_col,:]
    plt.imshow(result)
    plt.show()
