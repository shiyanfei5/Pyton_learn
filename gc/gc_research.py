
import sys
class item(object):
    def __init__(self,item = 1):
        self.item = item
a = [item(1),item(2)]
print(sys.getrefcount(a))
print(sys.getrefcount(a[1]))
b = a[1]
print(sys.getrefcount(a))
del(a)
#print(sys.getrefcount(a))
print(sys.getrefcount(b))
