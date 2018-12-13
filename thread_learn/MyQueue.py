from threading import Lock,RLock,Condition
from collections import deque

class MyQueue(object):

    def __init__(self , maxsize  ):
        self.maxsize = maxsize
        self._queue = deque()   #deque本身就是线程安全的
        self.get_lock = Lock()  # 该锁用于保证 读和写的互斥，即保证读时不发生写入


    def is_empty(self,):
        with self.get_lock:
            #占用该锁，防止有其他线程写入
            if len(self._queue) == 0:
                return True
            else:
                return False

    def is_full(self):
        #判断_queue的大小是否为maxsize
        with self.get_lock:
            #占用该锁，防止有其他线程写入
            if len(self._queue) == self.maxsize:
                return True
            else:
                return False

    def get_size(self):
        with self.get_lock:
            #占用该锁，防止有其他线程写入
            return len(self._queue)

    def put(self,value,block=True, timeout=None):
        with self.get_lock:
            pass

    def join(self):
        pass

    def task_done(self):
        pass

if __name__ == '__main__':
    pass