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
BATCH_SIZE = 64
TIME_SIZE = 28
INPUT_SIZE = 28
LR = 0.01
DOWNLOAD_MNIST = True if not os.path.isdir(datapath) else False

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

test_data = torchvision.datasets.MNIST(
    root = datapath,
    train = False,
    transform = torchvision.transforms.ToTensor(),
)
with torch.no_grad():
    test_x = Variable(test_data.data).type(torch.FloatTensor)[:2000]/255.
    test_y = test_data.targets.numpy().squeeze()[:2000]

class RNN(nn.Module):
    def __init__(self,):
        super().__init__()
        self.rnn = nn.LSTM(
            input_size = INPUT_SIZE,
            hidden_size = 64,
            num_layers = 1,
            batch_first = True,
        )
        self.out = nn.Linear(64, 10)

    def forward(self, x):
        r_out, (h_n, h_c) = self.rnn(x, None)
        out = self.out(r_out[:, -1, :])
        return out

rnn = RNN()
print(rnn)

optimizer = torch.optim.Adam(rnn.parameters(), lr=LR)
lossfunc = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):
        b_x = Variable(b_x.view(-1, 28, 28))
        b_y = Variable(b_y)

        output = rnn(b_x)
        loss = lossfunc(output, b_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 5 == 0:
            test_out = rnn(test_x)
            pred_y = torch.max(test_out, 1)[1].data.numpy().squeeze()
            accuracy = ((pred_y == test_y).sum().item())/(test_y.size)
            print('epoch:{} loss{:.4f} accuracy:{:.4f}'.format(epoch, loss.data, accuracy))
            # break

test_output = rnn(test_x[:10].view(-1, 28, 28))
pred_y = torch.max(test_output, 1)[1].data.numpy().squeeze()
print(pred_y,'pred')
print(test_y[:10],'real')