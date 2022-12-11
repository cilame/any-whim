# 创建定位训练的数据集脚本，该脚本会生成三种颜色的色块用于分类定位

import os, time, random

import cv2
import numpy as np

class Data:
    def __init__(   self, 
                    path = 'train_img',
                    imgfile = 'imgfile',
                    xmlpath = 'xmlpath',
                    minw = 416,
                    minh = 416,
                    maxw = 416,
                    maxh = 416,
                    channel = 3,
                    randomrect = (50,200,50,200), # minw,maxw,minh,maxh
                    randomcolor = {
                        'blue':  [255,0,0],
                        'red':   [0,0,255],
                        'green': [0,255,0],
                    },
                    bgcolor = [230,230,230],
                ):
        imgfile = imgfile if imgfile else ''
        xmlpath = xmlpath if xmlpath else ''
        self.imgpath = os.path.join(path, imgfile)
        self.xmlpath = os.path.join(path, xmlpath)
        if not os.path.isdir(self.imgpath): os.makedirs(self.imgpath)
        if not os.path.isdir(self.xmlpath): os.makedirs(self.xmlpath)
        self.minw = minw
        self.minh = minh
        self.maxw = maxw
        self.maxh = maxh
        self.channel = channel
        self.rangew = list(range(self.minw, self.maxw+1))
        self.rangeh = list(range(self.minh, self.maxh+1))
        self.randomw = list(range(randomrect[0], randomrect[1]+1))
        self.randomh = list(range(randomrect[2], randomrect[3]+1))
        self.color = randomcolor
        self.bgcolor = np.array(bgcolor)

        self.img_id = 0
        self.stamp = time.strftime("%Y%m%d", time.localtime())

    def make_img(self,):
        w = random.choice(self.rangew)
        h = random.choice(self.rangeh)
        img = np.ones((w, h, self.channel))
        img = img[:,:] * self.bgcolor
        return img, w, h

    def create_img(self,):
        w = random.choice(self.randomw)
        h = random.choice(self.randomh)
        img, iw, ih = self.make_img()
        x = random.choice(list(range(iw-w)))
        y = random.choice(list(range(ih-h)))
        c = random.choice(list(self.color))
        minx = x
        miny = y
        maxx = x+w
        maxy = y+h
        img[minx:maxx, miny:maxy] = self.color[c]
        folder = 'imgfile'
        filename, xmlname = self.create_name()
        realimgpath = os.path.join(self.imgpath, filename)
        realxmlpath = os.path.join(self.xmlpath, xmlname)
        xml = self.mkxml(folder,filename,realimgpath,iw,ih,self.channel,c,minx,miny,maxx,maxy)
        cv2.imwrite(realimgpath, img)
        with open(realxmlpath, 'w', encoding='utf-8') as f:
            f.write(xml)
        return realimgpath

    def create_imgs(self, number):
        for _ in range(number):
            self.create_img()

    def create_name(self,):
        imgname = '{}_{:>05}.png'.format(self.stamp, self.img_id)
        xmlname = '{}_{:>05}.xml'.format(self.stamp, self.img_id)
        self.img_id += 1
        return imgname, xmlname

    def mkxml(self,folder,filename,realpath,w,h,channel,clazz,miny,minx,maxy,maxx):
        # 非常注意的是，xml里面的 xmin,xmax 为纵坐标
        # 与我个人习惯的 x 代表横坐标有点不太一样，所以这里的wh也需要注意修改
        return r'''
<annotation>
    <folder>{}</folder>
    <filename>{}</filename>
    <path>{}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
</annotation>
'''.format(folder,filename,realpath,h,w,channel,clazz,minx,miny,maxx,maxy).strip()



def drawrect_and_show(imgfile, rect, text):# 只能写英文
    img = cv2.imread(imgfile)
    cv2.rectangle(img, rect[:2], rect[2:], (10,10,10), 1, 1)
    x, y = rect[:2]
    cv2.putText(img, text, (x,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,10,10), 1)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    d = Data(imgfile=None,xmlpath=None,
        minw = 416,
        maxw = 416,
        minh = 616,
        maxh = 616,
    )
    for i in range(2):
        img = d.create_img()
    drawrect_and_show(img, (20,20,100,100), 'hello world.')

    s = time.time()
    d.create_imgs(100)
    print(time.time() - s)