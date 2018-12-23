
import gc
import time

gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
def Test():

    class A:
        #pass
         def __del__(self):
             print("collect A",self)
    class B:
        #pass
         def __del__(self):
             print("collect B",self)

    a = A() #(1)
    b = B() #(2)
    c=A()   #(3)
    d=A()   #(4)
    a.next= b
    b.next = a
    con = []
    del a
    del b
    for i in range(300):
        con.append([i])
    del con
    con = []
    for i in range(300):
        con.append([i])
Test()
time.sleep(10)
print("解释器退出前的标记清除")


#
# if __name__ == '__main__':
#     import threading
#     thread_detail_url = threading.Thread( target = Test)
#     thread_detail_url.start()
#
#     print(" main-Thread Think is over")
#     time.sleep(100)
