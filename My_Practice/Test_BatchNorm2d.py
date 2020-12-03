'''
BatchNorm2d(num_features, eps=1e-05, momentum=0.1, affine=True)
    1 num_features： 来自期望输入的特征数，该期望输入的大小为'batch_size x num_features x height x width'
    2 eps： 为保证数值稳定性（分母不能趋近或取0）,给分母加上的值。默认为1e-5。
    3 momentum： 动态均值和动态方差所使用的动量。默认为0.1。
    4 affine： 一个布尔值，当设为true，给该层添加可学习的仿射变换参数。

BatchNorm2d原理、作用及其pytorch中BatchNorm2d函数的参数讲解 https://my.oschina.net/u/4274857/blog/4512852

'''

import torch

import torch.nn as nn

m = nn.BatchNorm2d(2, affine=True)  # 权重w和偏重将被使用   #affine默认为True,用于使用权重w和偏重b
input = torch.randn(1, 2, 3, 4)     #orch.randn 返回一个填充了正态分布中随机数的张量，均值为“0”，方差为“1”
output = m(input)

# print('m的第一个值',m.weight[0])
# print('m的第一个偏移值',m.bias[0])

print("输入图片：")
print(input)
print("归一化权重：")
print(m.weight)
print("归一化的偏重：")
print(m.bias)

print("归一化的输出：")
print(output)
print("输出的尺度：")
print(output.size())

# i = torch.randn(1,1,2)
print("输入的第一个维度：")
print(input[0][0])
firstDimenMean = torch.Tensor.mean(input[0][0])  # 通道均值
firstDimenVar = torch.Tensor.var(input[0][0], False)  # Bessel's Correction贝塞尔校正不会被使用
# 通道方差
print(m.eps)
print("输入的第一个维度平均值：")
print(firstDimenMean)
print("输入的第一个维度方差：")
print(firstDimenVar)

bacthnormone = \
    ((input[0][0][0][0] - firstDimenMean) / (torch.pow(firstDimenVar + m.eps, 0.5))) \
    * m.weight[0] + m.bias[0]
print(bacthnormone)