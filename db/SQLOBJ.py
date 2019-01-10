import requests
import chardet
import re
import functools
def unicode(a , _):
    return a



reg_proname = r'CREATE\s+OR\s+REPLACE\s+((FUNCTION)|(PROCEDURE]))\s+(?P<name>\w+?.*?\w*?)\s*\('
reg_perform = r'PERFORM\s+(?P<name>.*?)\s*\(.*\)'

def Check_type(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        name = re.search(reg_proname,content,re.IGNORECASE).group('name')
    except:
        name = 'table'
    depend = []

    if name != 'table':

        for li in re.findall(reg_perform, content,re.IGNORECASE):
            depend.append(li)
    return name,depend



class _BaseSQL:
    """
    基本SQL文件信息，编码，修改时间
    """
    def __init__(self,file_path):
        self._coding = ''
        self._file = ''
        self._last_time = ''
        self.do_time = ''

    def _detect_utf8(self):
        with open(self._file, 'rb') as f:
            result = chardet.detect(f.read())
            return result




class SqlTable:
    def __init__(self , file_path):
        pass

class SqlProcedure:
    def __init__(self,name,depend):
        self._name = name
        self._depend = depend   # 列表[]
        self.prioty = 0


    def _add_prioty(self,num=1):
        self.prioty += num

    def _depand_add_prioty(self,pro):
        self._add_prioty(pro.prioty+1)

    def __repr__(self):
        #return '%s-%s--%s'%(self._name,self._depend,self.prioty)
        return '%s-%s'%(self._name,self.prioty)


class ManagerSqlFile:
    def __init__(self,li):
        self.table = []
        self.procudure = li


    def __getitem__(self, item):
        """
         通过self['a']
        """
        for v in self.procudure:
            if item == v._name:
                return v
        return None


    def _get_prodepend(self , pro):
        """

        :param pro: 要查找的依赖的producer
        :return:
        """
        li = []
        for i in pro._depend:
            result = self.__getitem__(i)

            if result:
                li.append(result)
                result._depand_add_prioty(pro) #  加权，用于排序
        print(li)
        return li


    def _sort_pro(self):

        def cmp(a,b):
            if a.prioty < b.prioty:
                return 1
            elif a.prioty > b.prioty:
                return -1
            else:
                return 0


        self.procudure = list(sorted( self.procudure,key=functools.cmp_to_key(cmp)))

    def depend_sort(self):
        for item in self.procudure:
            print(item)
            self._get_prodepend(item)
        self._sort_pro()




if __name__ == '__main__':
    li = []
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档.txt','utf-8')
    a,b = Check_type(path)
    li.append( SqlProcedure( a,b ) )
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档2.txt', 'utf-8')
    a, b = Check_type(path)
    li.append(SqlProcedure(a, b))
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档3.txt', 'utf-8')
    a, b = Check_type(path)
    li.append(SqlProcedure(a, b))
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档4.txt', 'utf-8')
    a, b = Check_type(path)
    li.append(SqlProcedure(a, b))

    obj = ManagerSqlFile(li)
    obj.depend_sort()
    print(obj.procudure )