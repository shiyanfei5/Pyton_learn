import  weakref
import threading
import time
class A(object):
    def __init__(self,value):
        self.value = [value]

    def __del__(self):
        print("A object is deleted")

    def impl(self):
        def delete_callback(arg, b = self.value):
            b[0] = None
            print('self value is {}'.format(self.value))
            print(arg, "delete callback")

        a = A(1)
        t = threading.Thread(target=worker, args=(
            weakref.ref(a, delete_callback), self.value
        ))
        t.start()



def worker(ref , v):
    while 1:
        if v is not None:
            print("循环中")
            continue
        else:
            print("退出了")
            break


a = A(1)
a.impl()
exit()

