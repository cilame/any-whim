import torch
import torch.nn.functional as F
from torch.autograd import Variable

x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)
y = x.pow(2) + 0.2*torch.rand(x.size())
x = Variable(x)
y = Variable(y)

class Net(torch.nn.Module):
    def __init__(self, n, h, o):
        super().__init__()
        # n - number feature
        # h - number hidden
        # o - number output
        self.hidden = torch.nn.Linear(n, h)
        self.predict = torch.nn.Linear(h, o)

    def forward(self, x):
        x = F.relu(self.hidden(x))
        x = self.predict(x)
        return x

net = Net(1, 10, 1)
print(net)

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

# 对单个参数进行预测
t = torch.FloatTensor([[-0.8]])
v = Variable(t)
p = net(v)
print(p)