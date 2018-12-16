from concurrent.futures import ThreadPoolExecutor, Future , as_completed ,wait



import time

def get_html(times):
    time.sleep(times)
    print(" get page {} success".format(times))
    return times


executor = ThreadPoolExecutor(max_workers = 2)

urls = [1]
all_task = [executor.submit(get_html, (url)) for url in urls ]
#submit返回一个Future对象
print(all_task[0].result())


