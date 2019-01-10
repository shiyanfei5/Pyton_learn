from gc_learn.threadpool import MyThreadPool,as_completed
# from concurrent.futures import as_completed

import threading
import time

def get_html(times):
    time.sleep(times)
    print(" get page {} success ---{}-thread".format(times,threading.get_ident()))
    return times


executor = MyThreadPool(max_workers = 2)
# executor2 = MyThreadPool(max_workers = 3)
urls = [1,2,3,4,5]
all_task = [executor.submit(get_html, (url)) for url in urls ]

for future in as_completed(all_task):
    data = future.result()
del executor
time.sleep(100)

