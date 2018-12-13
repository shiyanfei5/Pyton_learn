from threading import Lock,RLock,Condition
from time import monotonic as time
from collections import deque

class MyQueue(object):

    def __init__(self , maxsize  ):
        self.maxsize = maxsize
        self._queue = deque()   #deque本身就是线程安全的
        self.get_lock = Lock()  # 该锁用于保证 读和写的互斥，即保证读时不发生写入
        self.con_not_full = Condition(self.get_lock)
        self.con_not_empty = Condition(self.get_lock)
        self.con_all_tasks = Condition(self.get_lock)
        self.unfished = 0

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

    def _get_size(self):
        """
        虽然deque线程安全，但是加上return 不一定线程安全，因为其可能在这个函数内被改写为多个操作
        """
        return len(self._queue)

    def _put(self,item):
        return self._queue.append(item)

    def _get(self):
        return self._queue.popleft()

    def put(self, item , block=True, timeout=None):
        """
        block:True Timeout:None or num
        block:False Timeout:不重要
        :return:
        """
        with self.con_not_full:         #拿到condition内部锁，用于保证读写互斥，防止并发
            if not block:
                if self._get_size() >= self.maxsize:
                    raise Exception("队列满了呜呜呜")
            else:

                if timeout is None:
                    # 唤醒后可能在condition的wait内竞争内部锁,还需要耗时,所以还要判断情况
                    while self._get_size() >= self.maxsize:
                       #说明队列满了，请等待
                        self.con_not_full.wait()
                else:
                    if timeout <= 0:
                        raise ValueError("'timeout' must be a positive number")
                    endtime = time() + timeout  #获取endtime时间应该为多少
                    # 若唤醒了该线程，接着wait继续运行，还需要先判断一次size，所以用while
                    while self._get_size() >= self.maxsize:
                        #唤醒后可能在condition的wait内竞争内部锁,还需要耗时
                        #重新计算等待时间
                        waiting_time = endtime - time()
                        #说明队列满了，请等待
                        self.con_not_full.wait(waiting_time)

                self._put(item)
                self.unfished += 1
                #每插入一个元素，唤醒一个为空等待获取元素的线程

                self.con_not_empty.notify()


    def get(self,block = True , timeout = None):
        with self.con_not_empty:
            if not block:
                if self._get_size() <= 0:
                    raise Exception("队列空了呜呜呜")
            else:

                if timeout is None:
                    while self._get_size() <= 0:
                        #唤醒后可能在condition的wait内竞争内部锁,还需要耗时
                        #唤醒后可能还是空，保险还是判断一下
                        self.con_not_empty.wait()
                else:
                    if timeout <= 0:
                        raise ValueError("'timeout' must be a positive number")
                    endtime = time() + timeout
                    while self._get_size() <= 0:
                        #唤醒后可能在condition的wait内竞争内部锁,还需要耗时
                        #重新计算等待时间
                        waiting_time = endtime - time()
                        self.con_not_empty.wait(waiting_time)

                self.con_not_full.notify() #先唤醒没关系，因为也没释放锁也得等着


                return self._get()


    def join(self):
        with self.con_all_tasks:
            while self.unfished > 0:
                self.con_all_tasks.wait()

    def task_done(self):
        with self.con_all_tasks:
            unfinished = self.unfished - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                #若没有任务了就唤醒全部join的线程
                self.con_all_tasks.notify_all()
            self.unfished = unfinished


if __name__ == '__main__':
    print(int(None))