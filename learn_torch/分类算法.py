# coding=utf-8
# pip install opencv-contrib-python torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple/

import os
import base64
import inspect
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

def read_imginfos(file, class_types_list):
    class_types = set()
    imginfos = []
    if class_types_list:
        class_types = list(class_types_list)
    else:
        for name in os.listdir(file):
            class_types.add(name)
        class_types = sorted(class_types)
    for clazz in os.listdir(file):
        clazzfilepath = os.path.join(file, clazz)
        for imgfile in os.listdir(clazzfilepath):
            imgfile = os.path.join(clazzfilepath, imgfile)
            fil = imgfile
            img = cv2.imdecode(np.fromfile(fil, dtype=np.uint8), 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
            img = cv2.resize(img, (40, 40))
            img = np.transpose(img, (2,1,0)) # [c,x,y]
            imginfo = {}
            imginfo['class'] = clazz
            imginfo['img'] = img
            imginfos.append(imginfo)
            # cv2.imshow('test', img)
            # cv2.waitKey(0)
    class_types = {tp: idx for idx, tp in enumerate(class_types)}
    return imginfos, class_types

# 生成 y_true 用于误差计算
def make_y_true(imginfo, class_types):
    img = imginfo['img']
    class_types.get(imginfo['class'])
    clz = [0.]*len(class_types)
    clz[class_types.get(imginfo['class'])] = 1.
    return torch.FloatTensor(clz)

def load_data(filepath, class_types_list=None):
    imginfos, class_types = read_imginfos(filepath, class_types_list)
    train_data = []
    print(len(imginfos))
    for imginfo in imginfos:
        train_data.append([torch.FloatTensor(imginfo['img']), make_y_true(imginfo, class_types)])
    return train_data, class_types

class MiniCNN(nn.Module):
    class ConvBN(nn.Module):
        def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
            super().__init__()
            padding   = (kernel_size - 1) // 2 if not padding else padding
            self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
            self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
            self.relu = nn.LeakyReLU(0.1, inplace=True)
        def forward(self, x): 
            return self.relu(self.bn(self.conv(x)))
    def __init__(self, class_types, inchennel=3):
        super().__init__()
        self.oceil = len(class_types)
        self.model = nn.Sequential(
            OrderedDict([
                ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  self.ConvBN(32, 64)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  self.ConvBN(64, 32)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  self.ConvBN(32, 8)),
                ('Flatten',   nn.Flatten()),
                ('Linear1',    nn.Linear(200, 64)),
                ('Linear2',    nn.Linear(64, self.oceil)),
            ])
        )
    def forward(self, x):
        x = torch.sigmoid(self.model(x))
        return x

def train(train_data, class_types):
    EPOCH = 1000
    BATCH_SIZE = 1000
    LR = 0.0001

    try:
        state = torch.load('net.pkl')
        net = MiniCNN(class_types)
        net.load_state_dict(state['net'])
        net.to(DEVICE)
        optimizer = state['optimizer']
        epoch = state['epoch']
        print('load train.')
    except:
        import traceback
        excp = traceback.format_exc()
        if 'FileNotFoundError' not in excp:
            print(traceback.format_exc())
        net = MiniCNN(class_types)
        net.to(DEVICE)
        optimizer = torch.optim.Adam(net.parameters(), lr=LR)
        epoch = 0
        print('new train.')

    # net = MiniCNN(class_types).to(DEVICE)
    mloss = miniloss(class_types).to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=LR)
    train_loader = Data.DataLoader(
        dataset=train_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )
    for epoch in range(epoch, epoch+EPOCH):
        print('epoch', epoch)
        for step, (b_x, b_y) in enumerate(train_loader):
            b_x = Variable(b_x).to(DEVICE)
            b_y = Variable(b_y).to(DEVICE)
            print(b_y.shape)
            loss = mloss(net(b_x), b_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        state = {'net':net.state_dict(), 'MiniCNNcode': inspect.getsource(MiniCNN), 'optimizer':optimizer, 'epoch':epoch+1, 'class_types':class_types}
        torch.save(state, 'net.pkl')
        try:
            with open('net.pkl', 'rb') as f:
                b64model = base64.b64encode(f.read()).decode()
            with open('net.b64', 'w') as f:
                f.write(b64model)
        except:
            pass
        print('save.')
    print('end.')

class miniloss(nn.Module):
    def __init__(self, class_types):
        super().__init__()
        self.clazlen = len(class_types)

    def forward(self, pred, targ, callback=None):
        loss = F.mse_loss(pred,targ,reduction='sum')
        global print
        print = callback if callback else print
        print(loss)
        return loss



















# coding=utf-8

import io
import base64
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

def read_img_by_base64(b64img, readtype=1):
    img = base64.b64decode(b64img.encode())
    image = cv2.imdecode(np.frombuffer(img, np.uint8), readtype)
    return image

def make_predict_func():
    def load_state(filename):
        '''
        > 如果想模型内容也写在单脚本里面，就用 base64 字符串保存和加载模型，就不用再额外管理模型文件了
        > 当然，建议这个 base64 的模型字符串也要稍微小一些，太大了，文本编辑器的单行太长都会很影响编辑器。
        > 模型几M以内还勉强可以的，只要编辑器加载和上下滑动不怎么卡顿就好了。
        '''
        # net_pkl = 'UEsDBAAACAgAAAAAAAAAAAAAAAAAAAA......'
        # state = torch.load(io.BytesIO(base64.b64decode(net_pkl.encode())))
        state = torch.load(filename)

        class_types = state['class_types']
        vars = {}
        exec(state['MiniCNNcode'], globals(), vars)
        MiniCNN = vars['MiniCNN']
        net = MiniCNN(class_types)
        net.load_state_dict(state['net'])
        net.to(DEVICE)
        net.eval()
        state['net'] = net
        return state
    def make_get_class_func(state):
        def get_class(filepath):
            net = state['net'].to(DEVICE)
            class_types = state['class_types']
            class_types = [i[0] for i in sorted(class_types.items(), key=lambda e:e[1])]
            if type(filepath) == str:
                img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
            else:
                img = filepath
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
            img = cv2.resize(img, (40, 40))
            img = np.transpose(img, (2,1,0)) # [c,x,y]
            x = torch.FloatTensor(img).unsqueeze(0).to(DEVICE)
            v = net(x)
            if USE_CUDA:
                v = v.cpu().detach().numpy()
            else:
                v = v.detach().numpy()
            v = v[0].tolist()
            r = class_types[v.index(max(v))]
            return r
        return get_class
    return make_get_class_func(load_state('net.pkl'))















# pip install cryptography flask vvv_rpc opencv-contrib-python torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple/

'''
本代码专门为小量图片分类使用的，生成模型很小，可以迅速单脚本化(请阅读 load_state 函数内注释)。
代码整体分为上面的两块，第一块主要是训练代码，第二块是预测代码
如果只用来预测，删掉训练部分代码，只留下后面的预测代码即可，代码做了独立可运行的处理
因为是定制了一下模型结构，所以模型很小，用 cpu 也可以轻松使用，所以 pytorch 用的就是 cpu 版本的

文件结构就用 二级文件夹作为类名，只要文件夹结构如下，修改 root 的地址，直接运行就可以

root
|
|-分类1
|  |- img1.png
|  |- img1.png
|  |- img1.png
|-分类2
|  |- img1.png
|  |- img2.png
|  |- img3.png
|-分类3
|  |- img1.png
|  |- img2.png
|  |- img3.png
'''

root = './分类完成20230208-1'

train_data, class_types = load_data(root)
train(train_data, class_types)

get_clazz = make_predict_func()

p = 0
q = 0
for clazz in os.listdir(root):
    filepath = os.path.join(root, clazz)
    for j in os.listdir(filepath):
        imgpath = os.path.join(filepath, j)
        t = get_clazz(imgpath)
        if t == clazz:
            p += 1
        else:
            # print(t, imgpath)
            q += 1
    print('正确', p, '错误', q, '正确率', p/(p+q))
