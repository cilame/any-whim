# -*- coding: cp936 -*-
from automine_win7 import *

"""
ʹ��ʱ�������ɨ��������Ļ�Ͽ��������ҳߴ���������С��״̬
��������ʱ�������ֶ�����
���������������ļ��ṹ��
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
0����ѡ�к�������ȷ��û���׵�����
-1����ȷ���Ƿ����׵�����

�ڽ����ֶ������Ժ�
ʹ�� train.py ����ѵ�������Զ�����
mycate_model.pickle��mytrain_model.h5 �������ļ�
"""


if not os.path.isdir('pic'):
    os.mkdir('pic')

screen = get_screen()
minepic = get_mine_pic(screen)

v = create_xywh(minepic)
for y,x,yw,xh in v:
    cv2.imwrite('pic/'+random_name(),minepic[y:yw,x:xh])
