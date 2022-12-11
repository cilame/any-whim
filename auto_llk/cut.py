from grid_spliter import GridSpliter

gridh,gridw = 11,19

import cv2
v = cv2.imread('temp.png')
grider = GridSpliter(v,gridh,gridw)
for i in range(gridh):
    for j in range(gridw):
        pict = grider.get_picmat_by_point(i,j)
        cv2.imwrite('pic_sample/%d_%d.png'%(i,j),pict)
