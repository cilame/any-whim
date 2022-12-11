# opencv 2.4

import cv2
import numpy as np

MIN_MATCH_COUNT = 10
img1 = cv2.imread('1.jpg')          # trainImage
img2 = cv2.imread('2.jpg')          # queryImage

def SIFT():
    sift = cv2.SIFT()
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des2,des1, k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
          good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        wrap = cv2.warpPerspective(img2, H, (img2.shape[1]+img2.shape[1] , img2.shape[0]+img2.shape[0]))

        matching = cv2.drawKeypoints(img1, [ kp1[m.trainIdx] for m in good ])
        matching2 = cv2.drawKeypoints(img2, [ kp2[m.queryIdx] for m in good ])
        rows, cols = np.where(wrap[:,:,0] >10)
        min_row, max_row = min(rows), max(rows) +1
        min_col, max_col = min(cols), max(cols) +1
        result = wrap[min_row:max_row,min_col:max_col,:]

        return matching, matching2, result

if __name__ == '__main__':
    matching, matching2, result = SIFT()
    cv2.imshow('img1.jpg',matching)
    cv2.imshow('img2.jpg',matching2)
    cv2.imshow('result.jpg',result)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
