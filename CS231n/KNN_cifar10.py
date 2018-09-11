import numpy as np
import os

def unpickle(cifar10):
    import pickle
    with open(cifar10, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

# 创建训练、测试样本
def CreatData():
    # 训练集
    data = []
    label = []
    for i in range(1, 6):
        batch_path = './cifar_10/cifar-10-batches-py/data_batch_%d'%(i)
        batch_dict = unpickle(batch_path)
        train_loader = batch_dict[b'data'].astype('float')
        train_label = np.array(batch_dict[b'labels'])
        data.append(train_loader)
        label.append(train_label)
    # 将5个训练样本batch合并为50000x3072，标签合并为50000x1
    # np.concatenate默认axis=0，为纵向连接
    TrainData = np.concatenate(data)
    TrainLabel = np.concatenate(label)
    # 测试集
    testpath = os.path.join('./cifar_10/cifar-10-batches-py', 'test_batch')
    test_dict = unpickle(testpath)
    TestData = test_dict[b'data'].astype('float')
    TestLabel = np.array(test_dict[b'labels'])

    return TrainData, TrainLabel, TestData, TestLabel

def KNN(Trdata, Trlabel, Tdata, k):
    num_train = Trdata.shape[0]
    num_test = Tdata.shape[0]
    dist = np.zeros((num_test, num_train))
    for i in range(num_test):
        dist[i] = np.reshape(np.sqrt(np.sum(np.square(Tdata[i] - Trdata), axis=1)), [1, num_train])
    predictlabel = np.zeros((num_test, 1))
    for i in range(num_test):
        nearest_k = Trlabel[np.argsort(dist[i])[:k]]
        print(nearest_k)
        predictlabel[i] = np.argmax(np.bincount(nearest_k))

    return predictlabel


traindata, trainlabel, testdata, testlabel = CreatData()
num_train = 10000
num_test = 5000

train_data = traindata[:num_train]
train_label = trainlabel[:num_train]
test_data = testdata[:num_test]
test_label = testlabel[:num_test]

num_test = test_data.shape[0]

# 设置k的取值
k_size = [3, 5, 10, 15, 20, 30, 40, 50]
k_ac = []
for k in k_size:
    PredictLabel = KNN(train_data, train_label, test_data, k)
    test_label = np.reshape(test_label, [num_test, 1])
    # 计算精度
    num_right = np.sum((PredictLabel==test_label).astype('float'))
    ac = (num_right / num_test) * 100
    k_ac.append(ac)
    print('K = %d -- accuracy = %.3f%%'%(k, ac))

best_size = np.argmac(k_ac)
max_ac = k_ac[best_size]
best_K = k_size[best_size]

print('\n\n最优准确率：%.3f%%\n最优K值：%d'%(max_ac, best_K))


    
