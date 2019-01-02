import threading
import gc

import time


class A(object):
    def __init__(self,value):
        self.value = value
    def __del__(self):
        print("xxx")


def fun(arg):
    print(arg)



def test():
    a = A(5)
    thread_1 = threading.Thread( target = fun , args=(a,))
    thread_1.start()


if  __name__ == '__main__':
    # test()
    # print("over")
    while True:
        work_item = A(5)
        if work_item is not None:
            print(A)
            # Delete references to object. See issue16284
            #del work_item
            time.sleep(5)
            print("over")
            continue