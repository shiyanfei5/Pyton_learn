#通过queue的方式进行线程间同步


#
# from thread_learn.MyQueue import MyQueue as Queue
import time
import threading


q = Queue(maxsize=200)

def get_detail_html(queue = q):
    while True:
        url = queue.get() #get是一个阻塞方法，队列为空时一直停着
        print(" get detail html  {url}----{th}".format(url = url,th = threading.get_ident()))
        time.sleep(2)
        #q.task_done()


def get_url_list(queue = q):
    while True:
        print(" put the url started")
        for i in range(5):
            queue.put("http://projextd/com/{id}".format(id = i))
        time.sleep(4)
        print("put the url end")

if __name__ == '__main__':
    thread_detail_url = threading.Thread( target = get_url_list)
    thread_detail_url.start()
    for i in range(6):
        html_thread = threading.Thread(target = get_detail_html)
        html_thread.start()
    #q.join()
    print(" main-Thread Think is over")
