#读懂python中的self https://blog.csdn.net/xrinosvip/article/details/89647884

#0 不使用self
class Person(object):
    pass
student = Person()
# print(student)
# print(Person)
student.name = "Gavin"     # 为实例变量 student 绑定 name 属性   类似于 赋值 操作
student.score = 100        # 为 其绑定  score 属性
print(student.name)
print(student.score)

'''
上述的方法虽然可以为类的实例变量绑定属性，但是不够方便和elegant , 由于类 可以起到模板的作用，故在创建实例的时候，可以将我们认为必须绑定 属性 强制填写进去，
在 python中，是通过 类中通常都会使用的一个方法，即def  __init__(self) 方法，在创建实例变量的时候，就把 name 和 score 等属性绑上去
'''

#1 使用self后
class Person1(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
student1 = Person1('Gavin', 100)  # 传入 __init__ 方法中需要的 参数
print(student1.name)
print(student1.score)

'''
注意：
1、__init__ 方法的第一个参数永远是 self ，表示创建的实例本身，因此，在 __init__ 方法的内部，就可以把各种属性绑定到 self，因为 self 就指向创建的 实例本身
2、使用了 __init__ 方法，在创建实例的时候就不能传入 空的参数了，必须传入与 __init__ 方法匹配的参数，但是 self 不需要传，python解释器会自己把实例变量传进去
'''

#2 在类中定义多个函数相互调用
class Person2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        sum = self.x + self.y
        return sum

    def square(self):
        squr = pow(self.x, 2) + pow(self.y, 2)
        return squr

    def add_square(self):
        # 在类中函数相互调用要加 self 不加 self ，会报错：
        c = self.add() + self.square()
        return c

student2 = Person2(3, 4)
print(student2.add())
print(student2.square())
print('--------- 我是可爱的分割线-----------')
print(student2.add_square())

'''
通过上述的例子可以看出，与普通的函数相比，在类中定义的函数只有两点点不同：
    1、第一个参数永远是 self ，并且调用时不用传递该参数
    2、在类中函数相互调用要加 self ，如上例中： c = self.add()+self.square(), 不加 self ，会报错： 函数未定义

    除此之外，类的方法和普通函数没甚区别，当然也可以使用 默认参数、可变参数和关键字参数，例子如下：
'''

#3 self的实例化      本来是 add() 函数的默认形参，通过将其实例化，就可以在其他函数体内调用 实例变量 z 被实例化以后，就可以利用实例化的方法访问它
#   其实 self 中存储的是 实例变量 和 实例函数 的属性，可以理解为一个字典（ dict ），如：{'name':'zhang','age':'18'}就是这些
class Person3(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, z=16):  # 设置 z 为实例变量，即 self.z = z, z 是 class 的一个成员了，而非普通局部变量
        self.z = z
        sum = self.x + self.y + z  # z虽然已被实例化，但是依然可以当作 普通变量来用
        return sum

    def square(self):
        squr = pow(self.x, 2) + pow(self.y, 2)
        return squr

    def add_square(self):
        c = self.add() + self.square() + self.z  # 调用实例变量 z
        return c

student3 = Person3(3, 4)
print(student.z)  #16  函数add 中的 z 被实例化以后，就可以利用实例化的方法访问它

#self到底是什么？
class Box(object):
    def __init__(self, boxname, size, color):
        self.boxname = boxname
        self.size = size
        self.color = color  # self就是用于存储对象属性的集合，就算没有属性self也是必备的

    def open(self, myself):
        print('-->用自己的myself，打开那个%s,%s的%s' % (myself.color, myself.size, myself.boxname))
        print('-->用类自己的self，打开那个%s,%s的%s' % (self.color, self.size, self.boxname))

    def close(self):
        print('-->关闭%s，谢谢' % self.boxname)


b = Box('魔盒', '14m', '红色')
b.close()
b.open(b)  # 本来就会自动传一个self，现在传入b，就会让open多得到一个实例对象本身，print看看是什么。
print(b.__dict__)  # 这里返回的就是self本身，self存储属性，没有动作。

'''
python 中一些特殊的实例变量：
    1、私有变量(private),只有内部可以访问，外部不能访问，私有变量是在名称前以两个下划线开头，如：__name，其实私有变量也不是完全不能被外部访问，不能直接访问是因为python解释器对外把
            __name 变量改成了 _类名__name,所仍然可以通过 _类名__name 来访问 __name .
    
    2、在Python中，变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量，所以，不能用__name__、__score__这样的变量名。
    
    3、以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”
'''