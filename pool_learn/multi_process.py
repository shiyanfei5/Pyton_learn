import multiprocessing
# from multiprocessing import Process

import msvcrt
from  multiprocessing import spawn
import os,time
import multiprocessing
import _winapi
from multiprocessing import util
# worker function
def worker(sign, lock=None):
    # lock.acquire()
    # lock.release()
    # time.sleep(1)
    print('xxx')
# Main

if __name__ == '__main__':
    plist = []
    # lock = multiprocessing.Lock()
    # for j in range(10):
    #     p = multiprocessing.Process(target=worker,args=('process',))
    #     plist.append(p)

    p = multiprocessing.Process(target=worker, args=('process',))
    p.start()
    p.join()
    print('xxxxxxxx')