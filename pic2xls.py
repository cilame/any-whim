# # py2
# import cv2
# from numpy import *
# from xlsxwriter.workbook import Workbook
# ROUND = 7.

# img = cv2.imread('123.jpg')
# y,x,ch = img.shape
# img = cv2.resize(img,(y/3,x/3))
# y,x,ch = img.shape

# t = Workbook('pic.xlsx')
# ts = t.add_worksheet()
# ts.set_default_row(height=1.8)
# ts.set_column(0,5000,.2)

# s = [(i,j) for i in xrange(y) for j in xrange(x)]
# for i,j in s:
#     color = rint(img[i,j]/ROUND)*ROUND
#     color = '#%02X%02X%02X' % tuple(color.tolist()[::-1])
#     fmat = t.add_format({'bg_color':color})
#     ts.write(i,j,'',fmat)
#     if j==0:print i,'/',y

# t.close()


# py3
import cv2
from numpy import *
from xlsxwriter.workbook import Workbook
ROUND = 7.

img = cv2.imread('123.jpg')
y,x,ch = img.shape
img = cv2.resize(img,(int(y/3),int(x/3)))
y,x,ch = img.shape

t = Workbook('pic.xlsx')
ts = t.add_worksheet()
ts.set_default_row(height=1.8)
ts.set_column(0,5000,.2)

s = [(i,j) for i in range(y) for j in range(x)]
for i,j in s:
    color = rint(img[i,j]/ROUND)*ROUND
    color = '#%02X%02X%02X' % tuple(map(int,color.tolist()[::-1]))
    fmat = t.add_format({'bg_color':color})
    ts.write(i,j,'',fmat)
    if j==0:print (i,'/',y)

t.close()
