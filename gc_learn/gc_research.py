#
# import sys
# import weakref
# import threading
# import time
# class item(object):
#     def __init__(self,item = 1):
#         self.item = item
# # a = [item(1),item(2)]
# # print(sys.getrefcount(a))
# # print(sys.getrefcount(a[1]))
# # b = a[1]
# # print(sys.getrefcount(a))
# # del(a)
# # #print(sys.getrefcount(a))
# # print(sys.getrefcount(b))
#
#
# def func(a):
#     print(" call back func")
#
# def fun2():
#     c = item(1)
#     print(sys.getrefcount(c))
#     d = weakref.ref(c,func)
#     print(sys.getrefcount(d()))
#     print(sys.getrefcount(c))
#
#
#
# def Func(wkr,a):
#     time.sleep(5)
#     print("线程内查看引用",sys.getrefcount(wkr()),sys.getrefcount(a),)
#
#     print(" thread func")
# it = item(1)
# it2 = item(2)
# # c = weakref.ref(it,func)
# thr = threading.Thread(target=Func,args=(weakref.ref(it,func),it2))
# print(sys.getrefcount(it2))
# thr.start()
# print(sys.getrefcount(it))
# t2 = weakref.ref(it,func)
# del it
# print('ok')
#
# def Fun3(arg = it2):
#     pass
# print(sys.getrefcount(it2))
# thr.join()
# print(sys.getrefcount(it2))
#
# def Func4(arg):
#     print('xxx',sys.getrefcount(arg))
# for attr in dir(Func4):
#     print(attr, getattr(Func4, attr))
# it4 = item(4)
# Func4(it4)
# #探究:1.何时引用技术会增加(作为函数参数,函数默认参数,类变量?)
# #   2.何时回收
# import gc
# gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
# def Test():
#
#     import sys
#     import time
#     class A:
#         #pass
#          def __del__(self):
#              print("collect A",self)
#     class B:
#         #pass
#          def __del__(self):
#              print("collect B",self)
#
#     #
#     # gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
#
#     a = A()
#     b = B()
#
#     c=A()
#     d=A()
#     time.sleep(1)
#
# gc.disable()
# Test()

import weakref
import sys
class A():
    def __del__(self):
        print("被回收")

def func(a):
    print(a,"回调")

a=A()
print(sys.getrefcount(a)-1)
b = weakref.ref(a,func)
del a

