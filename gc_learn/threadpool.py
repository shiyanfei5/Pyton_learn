from threading import Lock,Condition
from queue import Queue
import sys
import threading
import weakref
import itertools

import atexit

EXECUTOR = set()

def cleanExecutor():
    for item in EXECUTOR:
        for i in range(len(item._thread)):
            item._deque.put(None)
        for t in item._thread:
            t.join()
    print('exit over')

atexit.register( cleanExecutor)




class _Waiter(object):
    """
    设计一个waiter等待器。其被放入future对象中，waiter对象内存放所有的完成futures。：
    1.访问等待器的读取结果者：可以被等待器要求等待（event信号实现）,等待器中可存放所有的
    2.future对象控制等待器event
    """
    def __init__(self):
        self.con = threading.Condition() #对读取者控制
        self.finished_futures = []  #给读取结果集

    def add_result(self,future):
        with self.con:
            self.finished_futures.append(future)
            self.con.notify_all()

    def add_exception(self,future):
        with self.con:
            self.finished_futures.append(future)
            self.con.notify_all()

    def add_cancelled(self,future):
        with self.con:
            self.finished_futures.append(future)
            self.con.notify_all()

    def get_finished(self):
        """
         本方法提供给waiter对象的读取者，用于获取finished的线程
        非局部对象（公共资源）：waiter对象的finished_futures。。其可能被
        其他线程操作，所以需要带锁
        """
        with self.con:
            while self.finished_futures == []:
                # 注意使用 while设计。。唤醒后还要再进行判断，不符合再睡
                self.con.wait()

            else:

                result = self.finished_futures
                self.finished_futures = []
                return result

    def install_future(self,fs):
        '''
        本方法提供给操作 future对象的生产者，用于将锁注册到多个future对象内.
        需要注意 注册锁的时候future的状态可能是 已经运行完毕的
        :param fs:
        :return:
        '''
        for fut in fs:
            # 拿上fs中的future
            with fut._condition:    #拿锁防止被修改
                fut._waiters.append(self)
                #把 等待器放入所有的future对象中
                if fut._state in ['CANCELLED_AND_NOTIFIED','FINISHED']:
                    self.finished_futures.append(fut)




def as_completed(fs):
    """
    公共资源：future对象，但其已经设计的是线程安全
     由于这个函数的设计思想是完成多少future返回多少future直到没有，所以
    """
    fs = set(fs)
    waiter = _Waiter()
    waiter.install_future(fs)
    # waiter加载进入future
    while True:

        finish = waiter.get_finished()  #获取目前完成的future，队列
        for re in finish:
            yield re

        fs = fs - set(finish)    #表示剩下的future

        if list(fs) == []:      #为空后再进行读取被阻塞,所以要及时退出
            return 0












def worker(ref_excutor , workitem_queue):
    """
    本函数的功能是让调用此函数的线程去任务队列中取任务
    调用者：可能是不同线程
    公共资源：线程池的_deque队列,其本身已经线程安全
    需要考虑何时退出---拿到None退出False
    """
    while True:

        workitem = workitem_queue.get(block=True)   # 为空则阻塞
        if workitem is not None:
            workitem.run()  # 运行该任务
            continue
        # 当线程拿到None后，在以下条件退出
        #   1.线程池对象被gc回收了-----即弱引用返回None
        #   2.线程池主动调用
        print("chulaile")
        excutor = ref_excutor()

        # if (excutor is None) or ( excutor.shutdown is True):
        #     workitem_queue.put(None)
        #     return
        # del excutor
        return


##################################################################
class Myfuture(object):
    """
    future是一种设计思想，其代表了未来的异步计算结果，并提供接口给一些方法，一个future对象
    包含了如下的几种必要设计：
    1._state ：任务状态(pending,finished,cancel,cancelled_and_notified
    2._result:任务结果
    3._condition：由于future代表一个结果，所以其使用者包含 1.生产者线程（任务线程）
                2.消费者线程（获取结果线程），需要线程安全
    4._exception:任务过程中的异常
    5._waiters:外部接口。。这个最后再写
    """

    def __init__(self):
        self._state = 'PENDING'
        self._result = None
        self._exception = None
        self._waiters = []
        self._condition = Condition()  # 使用condition锁，因为要wait等待条件

    def set_exception(self, e):
        """
        设置exception结果
        :param e:
        :return:
        """
        with self._condition:  # 拿锁
            self._result = e
            for waiter in self._waiters:
                waiter.add_result(self)
                # 对waiter的处理,完成了放入等待器的finished队列
            self._condition.notify_all()

    def set_result(self, re):
        """
        给future设置结果。。。由于future对象需要考虑线程安全（由不同线程访问），所以修改
        公共资源的操作需要带锁
        """
        with self._condition:  # 拿锁
            self._result = re
            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()

    def set_running_or_notify_cancel(self):
        with self._condition:
            if self._state in ['PENDING']:
                self._state = 'RUNNING'
                return True
            if self._state in ['CANCELLED']:
                self._state = 'CANCELLED_AND_NOTIFIED'
                for waiter in self._waiters:
                    waiter.add_result(self)
                return False

    def result(self, timeout=None):
        """
        获取future结果，算是访问future对象。考虑线程安全，所以需要带锁
        """
        with self._condition:
            # 线程安全的设计 ，使用while而不是if
            # ['FINISHED','CANCELLED','CANCELLED_AND_NOTIFIED']:
            while self._state in ['PENDING']:  # 需要注意此处用while
                self._condition.wait(timeout)
            else:
                if self._exception:  # 存在异常
                    raise self._exception
                else:
                    return self._result

    def cancel(self):
        """
        取消获取future的操作
        :return:
        """
        with self._condition:
            # 线程安全的设计 ，使用while而不是if
            # ['FINISHED','CANCELLED','CANCELLED_AND_NOTIFIED']:
            if self._state in ['RUNNING', 'FINISHED']:
                return False
            if self._state in ['PENDING']:
                self._state = 'CANCELLED'
                self._condition.notify_all()
            return True


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
        EXECUTOR.add(self)

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

        work = MyWorkItem(func,*arg,**kwarg)
        # 不同线程都可以向同一个线程池中的同一个deque中submit任务

        # 向队列中添加任务，队列线程安全，支持并发没关系
        self._deque.put(work)
        # 之后管理 根据线程情况管理任务
        self._manage_thread_task()

        return work._future # 返回一个future对象

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

        def wreak_ref_call(_, queue=self._deque):
            print("进程池被收集----")
            queue.put(None)

        with self._lock:
            num = len(self._thread)
            if num < self._maxsize:
                thread_name = '{}_{}'.format(self._thread_name_prefix or self,num )
                t = threading.Thread(name=thread_name , target= worker, args=(
                    weakref.ref(self,wreak_ref_call) , self._deque
                ))

                t.daemon = True
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

    future = Myfuture

    def __init__(self, func, *arg, **kwarg):

        self.fn = func
        self.arg = arg
        self.kwarg = kwarg
        self._future = self.future()

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




