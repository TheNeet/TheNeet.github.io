import DataMnist
import random
import numpy as np

# 获取Mnist 数据集
TrainData, TrainLabel, TestData, TestLabel = DataMnist.Data()

# 初始化参数
num_train = 60000
num_test = 10000
num_target = 10
l = 0.000025 # 学习效率

W1 = np.zeros((100, 28*28)) 
stdv = 1 / 28
for i in range(100):
    for j in range(28 * 28):
        W1[i][j] = random.uniform(-stdv, stdv)
W2 = np.zeros((10, 100)) 
stdv = 1 / 10
for i in range(10):
    for j in range(100):
        W2[i][j] = random.uniform(-stdv, stdv)
relu = np.zeros((100, 100))
h2 = np.zeros((100, 1))
accuracy = 0
reg = 4.5

print('Train:')
for k in range(10):
    for i in range(num_train):
        data = TrainData[i].reshape(-1, 1) / 255
        label = np.zeros((10, 1))
        target = TrainLabel[i].astype(np.int)
        label[target][0] = 1
        h1 = np.dot(W1, data) # 100 * 1
    
        # 激活函数Relu，同时求导
        for j in range(100):
            if h1[j][0] > 0:
                h2[j][0] = h1[j][0]
                relu[j][j] = 1
            else:
                relu[j][j] = 0
                h2[j][0] = 0

        h3 = np.dot(W2, h2).astype('float') # 10 * 1
        h4 = np.exp(h3 - np.max(h3)).astype('float')
        h4 /= np.sum(h4)

        if np.max(h4) == h4[target][0] and np.max(h4) > 0.1:
            accuracy += 1

        loss = 0.0
        loss = -np.sum(np.log(h4)) / num_target + 0.5 * reg * np.sum(W2 * W2)

        # 求导并修改参数
        dW2 = np.dot(label - h4, h2.T) # 10 * 100
        dh2 = np.dot(W2.T, label - h4) # 100 * 1
        W2 = W2 - l * ( - dW2 + reg * W2)
        drelu = np.dot(relu, dh2) # 100 * 1
        dW1 = np.dot(drelu, data.T) # 100 * 28*28
        W1 = W1 - dW1 * l
    
    accuracy /= num_train
    #print(h4, '\ntarget:', target)
    print('Train of %d   accuracy:%.2f%%   loss:%.2f'%(k + 1, accuracy * 100, loss))
    accuracy = 0

print('\n\nTest:')
for i in range(num_test):
    data = TestData[i].reshape(-1, 1) / 255
    target = TestLabel[i].astype(np.int)
    h1 = np.dot(W1, data)
    for j in range(100):
        if h1[j][0] > 0:
            h2[j][0] = h1[j][0]
        else:
            h2[j][0] = 0
    h3 = np.dot(W2, h2)
    h4 = np.exp(h3 - np.max(h3)).astype('float')
    h4 /= np.sum(h4)
    if np.max(h4) == h4[target][0] and h4[target][0] > 0.1:
        accuracy += 1

accuracy /= num_test
print('Accuracy: %.2f%%'%(accuracy * 100))
