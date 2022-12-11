# -*- coding: utf-8 -*-
import numpy as np

class GridSpliter:
    '''
    最好还是选一个 mat.shape 的宽和长能分别被 h 和 w 整除的矩阵
    这样就能避免在这里进行不必要的修正
    这里的修正方式仅是以最简单的边缘填充切割方法，
        如果长度过小，则将图片 mat 的最右一列进行右填充
        如果长度过大，则将图片 mat 按修正长度进行右切
        如果宽度过小，则将图片 mat 的最下一列进行下填充
        如果宽度过大，则将图片 mat 按修正宽度进行下切
    '''
    def __init__(self, mat, h, w):

        assert float(h)==int(h) ,float(w)==int(w)
        self._mat = mat

        self._omh, self._omw = mat.shape[:2]
        self._h,  self._w  = int(h), int(w)
        
        self._gridh = int(round(float(self._omh)/self._h))
        self._gridw = int(round(float(self._omw)/self._w))

        self._tmh = self._gridh * self._h
        self._tmw = self._gridw * self._w

        if self._tmh > self._omh:
            self._gap_h = self._tmh - self._omh
            self._mat = np.vstack((self._mat, [self._mat[-1,:]]*self._gap_h))
        if self._tmh < self._omh:
            self._gap_h = self._tmh - self._omh
            self._mat = self._mat[:self._tmh,:]
        if self._tmw > self._omw:
            self._gap_w = self._tmw - self._omw
            self._mat = np.hstack(([self._mat]+map(lambda i:i[...,None],[self._mat[:,-1]]*self._gap_w)))
        if self._tmw < self._omw:
            self._gap_w = self._tmw - self._omw
            self._mat = self._mat[:,:self._tmh]
        self.lr_shape = self._creat_lrshape()

    def _creat_lrshape(self):
        hy,wx = np.mgrid[:self._h, :self._w]
        lhy = (hy * self._gridh)[...,None]
        lwx = (wx * self._gridw)[...,None]
        rhy = ((hy + 1) * self._gridh)[...,None]
        rwx = ((wx + 1) * self._gridw)[...,None]
        lr_shape = np.concatenate((lhy,lwx,rhy,rwx),axis=-1)
        return lr_shape


    def get_picmat_by_point(self, y, x):
        '''
        通过 grid 生成块的坐标点进行对切下来的图片简单返回
        '''
        ly,lx,ry,rx = self.lr_shape[y, x]
        return self._mat[ly:ry,lx:rx]

    def get_all_for_pred(self):
        '''
        该函数是用于神经网络训练好的函数进行批量预测时进行的简单包装
        '''
        hy,wx = np.mgrid[:self._h, :self._w]
        points = np.concatenate((hy[...,None],wx[...,None]),axis=-1).reshape((-1,2))
        mats = np.array([self.get_picmat_by_point(y,x)for y,x in points])
        return mats
        
        
if __name__ == "__main__":
    # test:
    omat = np.random.randint(0,9,(7,8))
    s = GridSpliter(omat, 3, 3)
##    print 'grid: (3,3).'
##    print '原始图片:',omat.shape
##    print omat
##    print '剪切图片:',s._mat.shape
##    print s._mat
##    print "获取的目标图片切片(grid=>3*3,point=>2,2):"
##    print s.get_picmat_by_point(2, 2)
##    print "gaps:",s._gap_h,s._gap_w
