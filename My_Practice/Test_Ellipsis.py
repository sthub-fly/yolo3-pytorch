'''
x[m,n]是通过numpy库引用数组或矩阵中的某一段数据集的一种写法，

m代表第m维，n代表m维中取第几段特征数据。

通常用法：
    x[:,n]或者x[n,:]
    x[:,n]表示在全部数组（维）中取第n个数据，直观来说，x[:,n]就是取所有集合的第n个数据,
    x[n,:]表示在n个数组（维）中取全部数据，直观来说，x[n,:]就是取第n集合的所有数据,
    x[:,m:n]，即取所有数据集的第m到n-1列数据

    x[...,0] 并不能替换为x[:,0] ，而是需要替换为x[:,:,0]
'''
#  x[:,0] 输出所有集合中的第一个元素
#  X[:, 1] 输出所有集合中的第二个元素
#  X[1, :] 输出第一个集合的所有元素
import numpy as np

X = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]])

#print(X[:, 0])  #[ 0  2  4  6  8 10 12 14 16 18]
#print(X[:, 1])  #[ 1  3  5  7  9 11 13 15 17 19]
#print(X[1, :])  #[2 3]

Y = np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20]])
#print(Y[:,1:3])
'''输出X数组中所有行第1到2列数据
[[ 1  2]
 [ 4  5]
 [ 7  8]
 [10 11]
 [13 14]
 [16 17]
 [19 20]]
'''
Z = np.array([[[1],[2],[3]], [[4],[5],[6]]])
print(Z[...,0])
#    [[1 2 3]
#    [4 5 6]]

print(Z[:,0]) #[[1] [4]]


print(Z[:,:,0])
#    [[1 2 3]
#    [4 5 6]]