import threading
import time
import gc
import weakref
import time


#
import atexit
# def _python_exit():
#     print("called python exit")
#     print(threading.active_count())
#     print('exit thread is {}'.format(threading.get_ident()))

atexit.register(_python_exit)
# gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)


    # while True:
    #     print(value)
    #     if value[0] is not None:
    #         time.sleep(1)
    #         print("执行中")
    #         continue
    #     else:
    #         time.sleep(5)
    #         print("over")
    #         break


def fun(ref,value):
    b = A(2)
    time.sleep(500)
    print('func thread is {}'.format(threading.get_ident()))

class A(object):
    def __init__(self,value):
        self.value = [value]
    def __del__(self):
        print(" object() is deleted")

    def Impl(self, type = True):

        def callback(a,b = self.value):
            b[0] = None
            print("callback is called--value is {}".format(b))


        thread_1 = threading.Thread\
            ( target = fun , args=(weakref.ref(self, callback), self.value))
        thread_1.setDaemon(type)
        thread_1.start()



print('main thread is {}'.format(threading.get_ident()) )
a = A(1)
a.Impl(False)
time.sleep(3)
del a
print(threading.active_count())