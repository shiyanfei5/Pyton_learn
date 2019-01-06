from gc_learn.threadpool import MyThreadPool
# from concurrent.futures import as_completed

import threading
import time

def get_html(times):
    time.sleep(times)
    print(" get page {} success ---{}-thread".format(times,threading.get_ident()))
    return times


executor = MyThreadPool(max_workers = 2)
# executor2 = MyThreadPool(max_workers = 3)
urls = [1,2,3,4,5,6,7,8,9]
all_task = [executor.submit(get_html, (url)) for url in urls ]
# all_task2 = [executor2.submit(get_html, (url)) for url in urls ]
# urls = [4]
# all_task = [executor.submit(get_html, (url)) for url in urls ]
# #submit返回一个Future对象
# # print(all_task[0].done()) #判断该任务是否执行成功，非阻塞
# print(all_task[0].result()) #获取该任务结果，默认是阻塞式
# executor.
# # del executor
# # print(all_task[1].cancel()) #futuren取消任务
# #线程池
# #1.主线程中可以获取某一个任务的状态或者返回值
# #2.当一个线程完成的是我们主线程能立即知道
# #3.futurens可以让多线程与多进程接口一一致
# #wait(all_task)#等待所有futures执行完
# # for item in all_task:
# #     item.cancel()
# # for future in as_completed(all_task):
# #     data = future.result()
# #     #print("get {} page".format('1'))
del executor
# print('xx {}'.format(all_task[4].result() ) )