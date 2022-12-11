# -*- coding: cp936 -*-
from automine_win7 import *

"""
使用时请务必让扫雷能在屏幕上看见，并且尺寸是缩到最小的状态
生成样本时候，请先手动分类
生成类似于如下文件结构：
pic-+->1+->1231233.png
    |   |->4321443.png
    |   |->1234121.png
    |   +->...
    +->2...
    +->3...
    ...
    +->8
    +->0
    +->-1
0代表选中后无数字确定没有雷的区域
-1代表不确定是否有雷的区域

在结束手动分类以后
使用 train.py 进行训练即可自动生成
mycate_model.pickle，mytrain_model.h5 这两个文件
"""


if not os.path.isdir('pic'):
    os.mkdir('pic')

screen = get_screen()
minepic = get_mine_pic(screen)

v = create_xywh(minepic)
for y,x,yw,xh in v:
    cv2.imwrite('pic/'+random_name(),minepic[y:yw,x:xh])
