import threading
import time
from threading import Lock,RLock,Condition,Semaphore
from queue import Queue
import threading
import time

semaphore = threading.Semaphore(2)

def func():
    while True:
        if semaphore.acquire():
            print(threading.currentThread().getName() + ' get semaphore')
            time.sleep(3)
        semaphore.release()



for i in range(4):
    t1 = threading.Thread(target=func)
    t1.start()