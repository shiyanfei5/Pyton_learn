import requests
import chardet
import re
import functools
def unicode(a , _):
    return a

reg_proname = r'CREATE\s+OR\s+REPLACE\s+((FUNCTION)|(PROCEDURE]))\s+(?P<name>\w+?.*?\w*?)\s*\('
reg_perform = r'PERFORM\s+(?P<name>.*?)\s*\(.*\)'


def check_type(file_name):
    '''
    检查file_name,然后查看其是否为那种类型的文件
    '''
    ret_obj = None
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        coding = chardet.detect(bytes(content)).get('encodinge')
    try:
        name = re.search(reg_proname,content,re.IGNORECASE).group('name')
    except:
        name = 'table'
    depend = []

    if name != 'table':
        for li in re.findall(reg_perform, content,re.IGNORECASE):
            depend.append(li)
        ret_obj = SqlProcedure()
    return name,depend



class BaseFILE:

    def __init__(self,file_path,coding):
        self._file = file_path
        self._coding = coding
        self._last_time = ''
        self.do_time = ''



class SqlTable(BaseFILE):

    def __init__(self , basefile ):
        self._basefile = basefile




class SqlProcedure(BaseFILE):
    """
    初始化Sql存储过程
    """
    def __init__(self, file_path, name, depend):
        super().__init__(file_path) # 初始化父类
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

    @classmethod
    def _check_file(cls):
        pass


class ManagerSqlFile:
    def __init__(self, li):
        self.table = []
        self.procudure = li
        self.inner_depend = {}

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
        pro: 要查找的依赖的producer
        """
        li = []
        for i in pro._depend:
            result = self.__getitem__(i)

            if result:
                li.append(result)
                result._depand_add_prioty(pro) #  加权，用于排序

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




class FileCreater:
    """
    统一封装文件检测接口

    """
    register_ftype = []  # 存放定义的文件类型对象,由生成类对象启动后注册进入

    @classmethod
    def _judge_file_type(cls , file_content, reg_ftype  ):
        """
        :param file_content: file_content为file的内容
        :param reg_ftype:
        :return:
        """
        result = reg_ftype.check_file(file_content)
        if result == None:
            return False
        else:
            return result

    @classmethod
    def _detect_coding(cls,file_content):
        result = chardet.detect( bytes(file_content) )
        return result.get('encoding')

    @classmethod
    def create_fileobj (cls, file_path ):
        with open(file_path,'r',encoding='utf-8') as file:
            content = file.read()
            coding = cls._detect_coding(content)
            for reg_type in cls.register_ftype:
                result = cls._judge_file_type(content, reg_type)
                if result:
                    return reg_type(file_path,coding,result)
            return None

    @classmethod
    def




if __name__ == '__main__':
    li = []
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档.txt','utf-8')
    a,b = check_type(path)
    li.append( SqlProcedure( a,b ) )
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档2.txt', 'utf-8')
    a, b = check_type(path)
    li.append(SqlProcedure(a, b))
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档3.txt', 'utf-8')
    a, b = check_type(path)
    li.append(SqlProcedure(a, b))
    path = unicode(r'D:\0.12.1-190108-to肖耀\新建文本文档4.txt', 'utf-8')
    a, b = check_type(path)
    li.append(SqlProcedure(a, b))

    obj = ManagerSqlFile(li)
    obj.depend_sort()
    print(obj.procudure )