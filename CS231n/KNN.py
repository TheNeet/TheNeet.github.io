import numpy as np
import os

# 读取数据
def unpickle(cifar10):
    import pickle
    with open(cifar10, 'rb') as Cifar10:
        dict = pickle.load(Cifar10, encoding='bytes')
    return dict

# 生成训练集
print('---生成训练集---')
for i in range(1, 6):
    batch_path = './cifar_10/cifar-10-batches-py/data_batch_%d'%(i)
    train_dict = unpickle(batch_path)
    train_load = train_dict[b'data'].astype('float')
    train_label = np.array(train_dict[b'labels'])
    if i == 1:
        TrainData = train_load
        TrainLabel = train_label
    else:
        TrainData = np.concatenate((TrainData, train_load))
        TrainLabel = np.concatenate((TrainLabel, train_label))   # 10000 * 3072

num_train = 50000
num_test = 10000
print('\n\n---生成测试集---')
batch_path = './cifar_10/cifar-10-batches-py/test_batch'
test_dict = unpickle(batch_path)
test_load = test_dict[b'data'].astype('float')
test_label = np.array(test_dict[b'labels'])
test_label = np.reshape(test_label, [num_test, 1])
K = 3
best_accuracy = 0
print(np.shape(TrainData))

from collections import Counter
for k in range(3, 20):
    PredictLabel = np.zeros((num_test, 1))
    for i in range(num_test):
        # 计算 【sqrt(sum(sqr(x1 - x2)))】欧式距离
        knn = np.reshape(np.sqrt(np.sum((test_load[i] - TrainData) ** 2, axis=1)), [1, num_train])
        closest_y = TrainLabel[np.argsort(knn)[:k]].flatten()
        c = Counter(closest_y)
        PredictLabel[i] = c.most_common(1)[0][0]
#        PredictLabel[i] = np.argmax(np.bincount(TrainLabel[np.argsort(knn)[:k]]))
    accuracy = np.sum(PredictLabel==test_label) / num_test * 100
    if best_accuracy < accuracy:
        K = k
        best_accuracy = accuracy
    print('K = %d -- accuracy = %.2f%%'%(k, accuracy))

print('best_K = %d -- It\'s best accuracy = %.2f%%'%(K, best_accuracy))
