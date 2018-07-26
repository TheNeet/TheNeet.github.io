import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

# 从MNIST中获取数据
transform = transforms.ToTensor()
# 训练集
train_dataset = datasets.MNIST(root='./data/', 
                               train=True, 
                               transform=transform, 
                               download=True)
# 测试集
test_dataset = datasets.MNIST(root='./data/',
                              train=False,
                              transform=transform)

# 装载数据
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                          batch_size=64, # 设置循环次数
                                          shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=64,
                                          shuffle=False)
input_size = 28 * 28 # 这个大小是怎么得到的
num_classes = 10
num_epochs = 10
hidden_size = 100

# 搭建神经网络
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear_1 = nn.Linear(input_size, hidden_size)
        self.fun = nn.ReLU()
        self.linear_2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.linear_1(x)
        out = self.fun(out)
        out = self.linear_2(out)
        return out

model = Model()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01) # lr为偏差值

def train(epoch):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data.view(-1, input_size)), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target) # output和target分别是什么内容呢？
        loss.backward()
        optimizer.step()
        if batch_idx % 200 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data[0]))

def test():
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = Variable(data.view(-1, 28 * 28), volatile=True), Variable(target)
        output = model(data)
        # sum up batch loss
        test_loss += criterion(output, target).data[0]
        # get the index of the max log-probability
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

for epoch in range(1, 10):
    train(epoch)
    test()
