import time
import gc
import sys
import weakref


class A(object):


    def fun_1(self):
        print("call fun_1")

    def __init__(self):
        print("xxx")

    def __del__(self):
        print("{} is delete".format(self) )

def fun(a):
    print(a())




gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
