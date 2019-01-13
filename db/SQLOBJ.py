
import chardet
import re
import os


def unicode(a , _):
    return a




class BaseFILE:

    def __init__(self, kw ):
        self._file =  kw.get('file')
        self._coding = kw.get('coding')
        self._operatetime = '999-999-99'
        self._do_time = ''

    def check_file(self,*arg,**kw):
        '''
        用于鉴别文件类型和信息，需要重载
        '''
        pass


    def __repr__(self):
        return '%s-%s-%s' %(self._file,self._coding,self._operatetime)

class SqlTable(BaseFILE):

    reg_pro = r'CREATE\s+OR\s+REPLACE\s+((FUNCTION)|(PROCEDURE]))\s+(?P<name>\w+?.*?\w*?)\s*\('
    reg_depend = r'PERFORM\s+(?P<name>.*?)\s*\(.*\)'

    def __init__(self , kw ):
        super().__init__(kw)
        self._name = os.path.split(self._file)[-1]

    @classmethod
    def check_file(cls, file_content):
        """
        用于检测文件类型并返回相关其他信息返回None，则不是该类文件，否则为该类文件
        """
        name = re.search(cls.reg_pro,file_content,re.IGNORECASE)
        if name:
            return None
        else:   #没搜索到
            return {'pass': 'pass'}


class SqlProcedure(BaseFILE):

    reg_pro = r'CREATE\s+OR\s+REPLACE\s+((FUNCTION)|(PROCEDURE]))\s+(?P<name>\w+?.*?\w*?)\s*\('
    reg_depend = r'PERFORM\s+(?P<name>.*?)\s*\(.*\)'

    def __init__(self, kw):
        super().__init__(kw) # 初始化父类
        self._depend = kw.get('depend')
        self._name = kw.get('name')
        self.prioty = 0

    def _add_prioty(self,num=1):
        self.prioty += num

    def _depand_add_prioty(self,pro):
        """
        依赖的pro的存储过程相加
        """
        self._add_prioty(pro.prioty+1)

    def __repr__(self):
        return '%s-%s-%s' %(self._name,self.prioty,self._depend)



    @classmethod
    def check_file(cls, file_content):
        """
        用于检测文件类型并返回相关其他信息返回None，则不是该类文件，否则为该类文件
        """
        name = re.search(cls.reg_pro,file_content,re.IGNORECASE)
        depend = []
        if name:
            for li in re.findall(cls.reg_depend, file_content, re.IGNORECASE):
                depend.append(li)
            return  {'name':name.group('name'), 'depend': depend}
        else:   #没搜索到
            return None






class FileFactory:
    """
    工厂，用于生成文件
    """
    register_ftype = [SqlProcedure,SqlTable]  # 存放定义的文件类型对象,由生成类对象启动后注册进入
    counter = 0

    @classmethod
    def _judge_file_type(cls , file_content, reg_ftype  ):
        """
        判断结果为None，则不在register里，否则在register_fytpe里
        """
        result = reg_ftype.check_file(file_content)
        if result == None:
            return False
        else:
            return result

    @classmethod
    def _detect_coding(cls,file_content):
        result = chardet.detect( bytes(file_content, encoding='utf-8' ) )
        return result.get('encoding')

    @classmethod
    def create (cls, file_path):
        init_dic = {}   # 生成对象所需的初始信息
        cls.counter += 1
        init_dic['file'] = file_path
        print ('%s-----处理%s'%(cls.counter,file_path) )
        with open(file_path,'r',encoding='utf-8') as file:
            content = file.read()
            coding = cls._detect_coding(content)
            init_dic['coding'] = coding
            for reg_type in cls.register_ftype:
                result = cls._judge_file_type(content, reg_type)

                if result:

                    init_dic.update(result)
                    return reg_type(init_dic)
            #  不行就返回基本类型
            return BaseFILE(init_dic)






if __name__ == '__main__':
    file_path = r'D:\0.12.1-190108-to肖耀\新建文本文档.txt'
    b = FileFactory.create(file_path)
    print(b)