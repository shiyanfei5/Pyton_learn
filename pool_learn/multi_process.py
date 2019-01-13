import multiprocessing
# from multiprocessing import Process



import os,time
import multiprocessing

# worker function
def worker(sign, lock):
    lock.acquire()
    lock.release()
    time.sleep(1)

# Main

if __name__ == '__main__':
    plist = []
    lock = multiprocessing.Lock()
    for j in range(5):
        p = multiprocessing.Process(target=worker,args=('process',lock))
        p.start()
        plist.append(p)
    p.join()