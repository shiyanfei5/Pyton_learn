# -*- coding: UTF-8 -*-

"""
1.管道是类似一个缓冲区队列，先进先出
2.os.read方法和os.write方法都是默认阻塞的，
"""

import os,time
def product(pipe_w):
    counter  = 0
    while True:
        counter += 1
        s = '%s---%s---%d^'%(os.getpid(),'produce' , counter)
        b_str = bytes(s,encoding='utf-8')
        os.write(pipe_w,b_str )
        time.sleep(2)


def consumer(pipe_r):
    while True:
        str = os.read(pipe_r,1024)  #read是阻塞方法。。。
        print(str)
        break
    os.close(pipe_r)

r,w = os.pipe()
pid = os.fork() # fork进程后用户级内存产生副本，还有文件描述符
if pid > 0:
    os.close(r)     # 父进程作为生产者，有w权限
    product(w)
else:
    os.close(w)    # 子进程作为消费者，有消费权限
    consumer(r)

t = os.mkfifo()
