import torch
import torch
import torch.utils.data as Data

BATCH_SIZE = 5

x = torch.linspace(1, 10, 10)
y = torch.linspace(10, 1, 10)

torch_dataset = Data.TensorDataset(x, y)
loader = Data.DataLoader(
    dataset = torch_dataset,
    batch_size = BATCH_SIZE,
    shuffle = True,
    # num_workers = 2, # windows 某些情况不可用这个参数
)

for eporch in range(3):
    for step, (batch_x, batch_y) in enumerate(loader):
        print('Epoch: ', step, batch_x, batch_y)
