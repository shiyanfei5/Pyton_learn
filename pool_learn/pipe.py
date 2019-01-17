import os
import time
import multiprocessing



# def worker(pipe_recv):
#     while True:
#         child_recv = pipe_recv.recv()
#         print(os.getppid(),os.getpid(),child_recv)
#
#
# if __name__ == '__main__':
#     child_recv,parent_send  = multiprocessing.Pipe()
#     p = multiprocessing.Process( target= worker , args=(child_recv,))
#     p.daemon = True
#     p.start()
#     print('父进程是',os.getpid())
#     while True:
#         str = input()
#         parent_send.send(str)
#         if str == 'Q':
#             break
#     print('main is over')


def worker(child):
    while True:
        child_recv = child.recv()
        print(os.getppid(),os.getpid(),child_recv)
        str = input()
        child.send(str)



if __name__ == '__main__':
    child,parent  = multiprocessing.Pipe(False)
    p = multiprocessing.Process( target= worker , args=(child,))
    p.daemon = True
    p.start()
    print('父进程是',os.getpid())
    while True:
        str = input()
        parent.send(str)
        if str == 'Q':
            break
        time.sleep(100)
        str = parent.recv()
        print('主进程', os.getpid(), str)

    print('main is over')
