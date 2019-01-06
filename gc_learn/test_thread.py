import threading
import time
import atexit

def quit():
    time.sleep(1)
    print("quit")

atexit.register(quit)
class A(object):
    def __init__(self):
        print('object is created')
    def __del__(self):
        print("A object is deleted")

class Func(threading.Thread):
    def run(self):
        a = A()
        time.sleep(1.000001)
        print("jieshu")

    def __del__(self):
        print("this is over")

def test():
    t1 = Func()
    t1.setDaemon(True)
    t1.start()

test()
b=A()
# # time.sleep(5)
# print("xxxx")

