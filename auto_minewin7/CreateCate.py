# -*- coding: utf-8 -*-
import os, pickle
from collections import OrderedDict

import cv2
import numpy as np

class CreateCate(object):

    """
    categorical_crossentropy 训练的样本生成器

    功能:
        读取根据文件夹名字进行图片的读入
        *生成对应的完整的 one-hot 训练数据集
        *将其作为可进行训练的 numpy 数据类型直接使用
    
    e.g: >>>s = CreateCate(picpath) # 注意默认参数 create=True
         >>>s.x # 可直接使用。  s.x.shape->(n, height, width, channel)
         >>>s.y # 可直接使用。  s.y.shape->(n, s.class_num) one-hot 数据型
    
    在实例化的时候即将该路径下的文件夹名字作为类名
    支持多路径功能
    """

    def __init__(self, *args, **kw):
        """
        *args：
            仅接受图片类文件路径
            
            picpath1+>classA+>pic1
                    |       |>pic2
                    |       +>pic3
                    +>classB...
                    +>classC...

            picpath2+>classD...
                    +>classB...
                    +>classC...

            s.classes = [classA, classB, classC, classD]
            
            可以直接多填
            也可以填写一个list
            e.g: CreateCate(picpath1,picpath2,**kw)
                 CreateCate([picpath1,picpath2],**kw)

        **kw:
            create = True
            是否在实例化时候直接读取数据
            
            over2show = 200
            读取图片数据时候，超过多少将进行读取进度的显示
            
            nptype = np.float32
            读取数据的整体格式
        """
        self.__args = args
        self.__create = kw.get('create', True)
        self.__over2show = kw.get('over2show', 200)
        self.__nptype = kw.get('nptype', np.float32)
        self.classes = self.__path2class()
        self.class_num = len(self.classes)
        self.__files = self.__get_paths_tree()
        self.__filters = ['jpg', 'png',]
        self.__cates = map(tuple, np.eye(self.class_num).tolist())
        self.__cates2class = OrderedDict(zip(self.__cates, self.classes))
        self.__class2cates = OrderedDict(zip(self.classes, self.__cates))
        if self.__create:
            self.__create_XnY()
        else:
            self.get_XnY = self.__get_XnY

    def __get_paths(self):
        if not self.__args:
            self.__create = False
            return self.__args
        typestrs = all(map(lambda i:type(i)==str,self.__args))
        typelist = (len(self.__args)==1 and (type(self.__args[0])==list or type(self.__args[0])==tuple))
        if not typelist and not typestrs:
            raise 'args only accept some picpath string or a picpath list.'
        if typestrs: paths = self.__args
        if typelist: paths = self.__args[0]
        return paths

    def __get_paths_tree(self):
        paths = self.__get_paths()
        classes_paths = {}.fromkeys(self.classes)
        for path in paths:
            for i in filter(lambda i:os.path.isdir(os.path.join(path,i)), os.listdir(path)):
                if not classes_paths[i]:
                    classes_paths[i] = [os.path.join(path,i)]
                else:
                    classes_paths[i] += [os.path.join(path,i)]
        return classes_paths

    def __path2class(self):
        paths = self.__get_paths()
        classes = set()
        for path in paths:
            for i in filter(lambda i:os.path.isdir(os.path.join(path,i)), os.listdir(path)):
                classes.add(i)
        return list(classes)


    def save_mapdict(self, name):
        """
        将类名以及产生的 one-hot 数据进行对应的 mapdict 进行保存
        
        e.g:
            >>>s.save_mapdict('cls.pickle')

        会生成 cls.pickle 文件
        """
        pickle.dump(self.__cates2class, open(name,'w'))


    @staticmethod
    def load_mapdict(name):
        """
        将类名以及产生的 one-hot 数据进行对应的 mapdict 进行读取
        e.g:
            >>>cates2class = s.save_mapdict('cls.pickle')

        会读取 cls.pickle 文件
        """
        return pickle.load(open(name))

    @staticmethod
    def get_class_by_cate(cates2class, l):
        """
        通过读取 mapdict 以及一个 one-hot 查找对应的类名
        因为该函数为静态函数，所以使用时可以不图片加载地址

        e.g:
            >>>s = CreateCate()
            >>>cates2class = s.load_mapdict('cls.pickle')
            >>># 通过 load_mapdict 加载 cls.pickle 文件
            >>>s.get_class_by_cate(cates2class, l)
        
        """
        s = np.array(l).ravel()
##        s[s>=.5], s[s< .5] = 1., 0.
        s[s==np.max(s)],s[s!=np.max(s)] = 1., 0.
        cate = tuple(s.tolist())
        return cates2class[cate]

##    def get_class_by_cate_test(self, l):
##        s = np.array(l).ravel()
##        s[s>=.8], s[s< .8] = 1., 0.
##        cate = tuple(s.tolist())
##        return self.__cates2class[cate]

    def __create_sample(self, picpath):
        pics = [os.path.join(picpath, i) \
                for i in os.listdir(picpath) \
                if lambda b:b[-3:].lower()in self.__filters]
        return pics

    def __get_allnum(self):
        allnum = 0
        for cls in self.classes:
            for picpath in self.__files[cls]:
                allnum += len(os.listdir(picpath))
        return allnum
        
    def __create_samples(self):
        num = 1
        show = False
        allnum = self.__get_allnum()
        showp = map(int, (np.arange(0,1.1,.1)* allnum).tolist())
        if allnum > self.__over2show: show = True
        
        x, y = [], []
        for cls in self.classes:
            for picpath in self.__files[cls]:
                for pic in self.__create_sample(picpath):
                    if show and num in showp:
                        print ('[*]%6d num. %6.2f%% pics has load.') % (num, float(num)/allnum*100)
                    x += [cv2.imread(pic).astype(self.__nptype)]
                    y += [self.__class2cates[cls]]
                    num += 1
        return np.array(x), np.array(y).astype(self.__nptype)

    def __create_XnY(self):
        self.x, self.y = self.__create_samples()
        if len(self.x.shape) == 1:
            print '[*]WARNING! self.x.shape:%s'%str(self.x.shape)
            print '[*]you must ensure all pic shape is same.'

    def __get_XnY(self):
        if not (hasattr(self, 'x') or hasattr(self, 'x')):
            self.__create_XnY()
        return self.x, self.y

