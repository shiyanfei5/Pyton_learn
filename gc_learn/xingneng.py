import time
import gc

gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
s_time = time.time()
data = range(1,50000000)
wdict = dict(zip(data,data))
print(time.time()-s_time)