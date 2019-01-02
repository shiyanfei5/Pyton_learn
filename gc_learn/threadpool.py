from threading import Lock
from queue import Queue
import sys
import threading
import weakref
import itertools
from gc_learn.myfuture import Future

def worker(ref_excutor , workitem_queue):
    """
    本函数的功能是让调用此函数的线程去任务队列中取任务
    调用者：可能是不同线程
    公共资源：线程池的_deque队列,其本身已经线程安全
    需要考虑何时退出---拿到None退出
    """
    while True:
        excutor = ref_excutor()
        print(sys.getrefcount(excutor)-1)
        workitem = workitem_queue.get(block=True)   # 为空则阻塞
        print(workitem)
        if workitem is not None:
            workitem.run()  # 运行该任务
            break
        # 当线程拿到None后，在以下条件退出
        #   1.线程池对象被gc回收了-----即弱引用返回None
        #   2.线程池主动调用
        print("chulaile")


        if ( excutor is None) or ( ref_excutor.shutdown is True):
            workitem_queue.put(None)
            return






class MyThreadPool(object):
    _counter = itertools.count().__next__
    """
    ThreadPool是一个线程安全的对象，支持不同线程处理同一个线程池对象
    所以，必须有锁;另外，线程池需要一个线程安全的队列来存放任务
    这个队列支持用不同线程并发加入任务，所以选用线程安全的deque
    """
    def __init__(self,max_workers=None , thread_name_prefix=''):
        self._maxsize = max_workers # maxsize表示最大的线程数
        self._shutdown = False   #表示是否为shutdown
        self._lock = Lock()
        self._deque = Queue() # 任务队列,标志位为None时结束
        # 因为要做线程同步，，比如没有任务让该线程等一下wait。。所以只能使用Queue
        self._thread = []
        # 用于存放开启的线程
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
        with self._lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
        future = Future() # future用来表示最后的结果
        work = MyWorkItem(future,func,*arg,**kwarg)
        # 不同线程都可以向同一个线程池中的同一个deque中submit任务

        # 向队列中添加任务，队列线程安全，支持并发没关系
        self._deque.put(work)
        # 之后管理 根据线程情况管理任务

        self._manage_thread_task()
        print(sys.getrefcount(self) - 1)
        return future # 返回一个future对象

    def _manage_thread_task(self):
        """
        1.当前线程池数量<  max，开新线程,执行函数
        2.否则无所动
        思考：
        1.功能如上
        2.调用者：可以是不同线程调用该函数
        3.公共资源：线程池对象中_thread，需要要拿到他的数量，并插入所以需要加锁
        """
        # 回调函数，线程池对象被回收后触发，来放入None
        def wreak_ref_call(_,queue = Queue()):
            print("进程池被收集----")
            queue.put(None)


        with self._lock:
            num = len(self._thread)
            if num < self._maxsize:
                thread_name = '{}_{}'.format(self._thread_name_prefix or self,num )
                t = threading.Thread(name=thread_name , target= worker, args=(
                    weakref.ref(self,wreak_ref_call) , self._deque
                ))

                t.daemon = False
                t.start()
                self._thread.append(t)



    def shutdown(self,wait=True):
        """
        功能：调用本函数的线程 关闭线程池对象不再接收新任务，
        wait：为True时调用的线程等待 任务队列中的任务执行完再运行
                为False时调用本函数的线程立马执行完退出本函数
        """
        with self._lock:
            self._shutdown = True
        self._deque.put(None)   # 给队列中放入一个None，引发连锁反应
        if wait:
            for t in self._thread:
                t.join()
                #等待



class MyWorkItem(object):
    def __init__(self, future, func, *arg, **kwarg):
        self._future = future
        self.fn = func
        self.arg = arg
        self.kwarg = kwarg


    def run(self):
        if not self._future.set_running_or_notify_cancel():
            return
        #
        try:
            result = self.fn(*self.arg, **self.kwarg)

        except BaseException as exc:
            self._future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None
        else:
            self._future.set_result(result)

class Myfuture(object):
    def __init__(self):
        pass




