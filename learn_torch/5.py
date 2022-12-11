import os

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.utils.data as Data
import torchvision

# 获取用户目录，将需要下载的测试数据文件存放在用户目录下面，防止git提交时候数据过大。脚本也能方便的处处运行。
home = os.environ.get('HOME')
home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
workerpath = os.path.join(home, 'learn_pytorch')
datapath = os.path.join(workerpath, 'mnist')
if not os.path.isdir(workerpath):
    os.makedirs(workerpath)
print('datapath:', datapath)

EPOCH = 1
BATCH_SIZE = 50
LR = 0.001
DOWNLOAD_MNIST = True if not os.path.isdir(datapath) else False

# 训练数据
train_data = torchvision.datasets.MNIST(
    root = datapath,
    train = True,
    transform = torchvision.transforms.ToTensor(),
    download = DOWNLOAD_MNIST,
)
train_loader = Data.DataLoader(
    dataset=train_data,
    batch_size=BATCH_SIZE,
    shuffle=True,
    # num_workers=2, 
)

# 测试数据
test_data = torchvision.datasets.MNIST(root=datapath, train=False)
with torch.no_grad():
    test_x = Variable(torch.unsqueeze(test_data.data, dim=1)).type(torch.FloatTensor)[:2000]/255.
    test_y = test_data.targets[:2000]

class CNN(nn.Module):
    def __init__(self,):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1,out_channels=16,kernel_size=5,stride=1,padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16,out_channels=32,kernel_size=5,stride=1,padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.out = nn.Linear(32*7*7, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1) # 类似 flat
        x = self.out(x)
        return x

cnn = CNN()
print(cnn)

optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
lossfunc = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):
        b_x = Variable(b_x)
        b_y = Variable(b_y)

        output = cnn(b_x)
        loss = lossfunc(output, b_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step&50 == 0:
            test_output = cnn(test_x)
            pred_y = torch.max(test_output, 1)[1].data.squeeze()
            accuracy = ((pred_y == test_y).sum().item())/(test_y.size()[0])
            print('EPOCH:', epoch, 'loss:{:.4f}'.format(loss.data), 'accuracy:{:.4f}'.format(accuracy))

test_output = cnn(test_x[:10])
pred_y = torch.max(test_output, 1)[1].data.numpy().squeeze()
print(pred_y,'pred')
print(test_y[:10].numpy(),'real')
