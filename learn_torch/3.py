import torch
import torch.nn.functional as F
from torch.autograd import Variable

x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)
y = x.pow(2) + 0.2*torch.rand(x.size())
x = Variable(x)
y = Variable(y)

def save():
    net = torch.nn.Sequential(
        torch.nn.Linear(1, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 1),
    )
    optimizer = torch.optim.SGD(net.parameters(), lr=0.5)
    lossfunc = torch.nn.MSELoss()
    for t in range(100):
        prediction = net(x)
        loss = lossfunc(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if t % 10 == 0:
            print('learn number:{}'.format(t), loss)
    torch.save(net, 'net.pkl') # 保留全部，且保留结构，直接加载即可使用
    torch.save(net.state_dict(), 'net_params.pkl') # 仅保留参数，需要先搭建结构才能加载进去

def restore_net():
    net = torch.load('net.pkl')
    return net

def restore_params():
    net = torch.nn.Sequential(
        torch.nn.Linear(1, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 1),
    )
    net.load_state_dict(torch.load('net_params.pkl'))
    return net

# 对单个参数进行预测
t = torch.FloatTensor([[-0.8]])
v = Variable(t)

save()
net1 = restore_net()
net2 = restore_params()
p = net1(v)
print(p)
p = net2(v)
print(p)

import os
os.remove('net.pkl')
os.remove('net_params.pkl')