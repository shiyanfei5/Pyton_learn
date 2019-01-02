from threading import Lock,RLock,Condition
from queue import Queue
from collections import deque
import threading

deque = deque

class MyThreadPool(object):
    """
    ThreadPool是一个线程安全的对象，支持不同线程处理同一个线程池对象
    所以，必须有锁;另外，线程池需要一个线程安全的队列来存放任务
    这个队列支持用不同线程并发加入任务，所以选用线程安全的deque
    """
    def __init__(self,maxsize=None , thread_name_prefix=''):
        self._maxsize = maxsize #maxsize表示最大的线程数
        self._lock = Lock()
        self._deque = deque()
        self._thread = []
        #用于存放开启的线程
        self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))

    def submit(self,func,*arg,**kwarg):
        """
        1.往线程池的deque中放workitem（生产）
        2.管理（创建或调度）线程用来从dequeu中取任务执行（消费）
        本函数需要考虑多线程的并发，由于dequeu的默认操作时线程安全
        所以其put或get是安全的，

        函数设计：
        1、考虑其功能
        2.考虑其调用者是哪一个线程
        3.考虑调用过程中公共的对象
        """
        future = Myfuture() #future用来表示最后的结果
        work = MyWorkItem(future,func,*arg,**kwarg)
        #不同线程都可以向同一个线程池中的同一个deque中submit任务

        #向队列中添加任务，队列线程安全，支持并发没关系
        self._deque.append(work)
        #之后管理 根据线程情况管理任务

        self._manage_thread_task()
        return future #返回一个future对象

    def _manage_thread_task(self):
        """
        1.当前线程池数量<  max，开新线程,执行函数
        2.否则无所动
        思考：
        1.功能如上
        2.调用者：可以是不同线程
        3.公共资源：线程池对象中_thread，要拿到他的数量，并插入所以需要加锁
        """
        with self._lock:
            num = len(self._thread)
            if  num < self._maxsize:
                thread_name = '{}_{}'.format(self._thread_name_prefix or self,num )
                t = threading.Thread(name=thread_name , target= ??, )

                t.daemon = True
                t.start()
                self._thread.append(t)


class MyWorkItem(object):
    def __init__(self,future,func,*arg,**kwarg):
        self._future = future
        self.func = func
        self.arg = arg
        self.kwarg =


class Myfuture(object):
    def __init__(self):
        pass