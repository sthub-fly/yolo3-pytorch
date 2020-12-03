'''
pytorch之torch.nn.Conv2d()函数详解  https://blog.csdn.net/qq_34243930/article/details/107231539
'''
import torch

x = torch.randn(3,1,5,4)
print(x)

conv = torch.nn.Conv2d(1,4,(2,3))
res = conv(x)


print('---------')
print(res.shape)    # torch.Size([3, 4, 4, 2])
