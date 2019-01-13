import os
import functools
from db.SQLOBJ import FileFactory,SqlProcedure,SqlTable
from db.test import find_files
import time
from  db.ELKQUERY import ElkQuery,ELK_MAIN


def now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class ManagerSqlFile:
    def __init__(self,*file):

        self.table = []
        self.procedure = []
        self.inner_depend = {}  # {'pro',[xx,xx]}
        print('%s********************开始加入存储过程***********************'%(now_time()) )
        for i in file:
            self.add_sqlfile(FileFactory.create(i))
        print('%s*****************加入过程完毕，共加入存储过程%s,表%s***************'%(now_time(),len(self.procedure),len(self.table)))
        self.depend_sort()
        print('%s********************Manager管理器排序完成*************************'%(now_time()) )


    def __getitem__(self, item):
        """
         通过self['a'] 选择procesure.obj['_name']
        """
        for v in self.procedure:
            if item == v._name:
                return v
        return None

    def _add_check(self,sqlobj):
        for item in self.procedure:
            if item._file == sqlobj._file:
                raise Exception("无法添加同一个文件%s" % sqlobj._file)

            if isinstance(item, SqlProcedure) and sqlobj._name == item._name:
                raise Exception("无法刷新同一个存储过程%s" % sqlobj._name)

        return True

    def add_sqlfile(self,sqlobj):
        """
        添加sqlfile到Manage，注意table类的file不进行检查

        """
        if self._add_check(sqlobj):
            if isinstance(sqlobj ,SqlProcedure ):
                self.procedure.append(sqlobj)
                print( '      加入存储过程成功%s'%sqlobj._name)
            elif isinstance(sqlobj, SqlTable):
                self.table.append(sqlobj)


    def _get_innerdepend(self , pro):
        """
        pro: 要查找的依赖的producer,并加权
        """
        li = []
        for i in pro._depend:   # 迭代 pro 的依赖，i为其名字
            result = self[i]    # 获取 依赖的存储过程

            if result:
                li.append(result)
                result._depand_add_prioty(pro) #  加权，用于排序

        s = [item._name  for item in li]
        if s:
            self.inner_depend.update({ pro._name:s})
        return li


    def _sort_pro(self):

        def cmp(a,b):
            if a.prioty < b.prioty:
                return 1
            elif a.prioty > b.prioty:
                return -1
            else:
                return 0
        self.procedure = list(sorted(self.procedure, key=functools.cmp_to_key(cmp)))

    def depend_sort(self):
        for item in self.procedure:
            self._get_innerdepend(item)
        self._sort_pro()



class Operator:
    def __init__(self , file_path):
        self.file_list = find_files(file_path)
        self.manager = ManagerSqlFile(*self.file_list)
        self.manager.depend_sort()  # 完成后最后进行排序


    def make_prepare_list(self):

        with open('list.txt','a+',encoding='utf-8') as file:
            str = '\n%s-----------上线文件夹总目录文件数%s---存储过程数目%s ---------------- \n'\
                  %(now_time() ,len(self.file_list),len(self.manager.procedure))
            file.writelines(str)
            for i in range(len(self.file_list)):
                str = '%s  %s \n' %(i+1, self.file_list[i],)
                file.writelines(str)
            str = '\n--存储过程与依赖信息如下所示：\n'
            file.writelines(str)
            for i in range(len(self.manager.procedure)):
                procedure = self.manager.procedure[i]
                str = '%s 位置:%s  过程名:%s \n   依赖存储过程:%s    \n   本次依赖过程:%s\n'%\
                      (i+1, procedure._file, procedure._name, procedure._depend,self.manager.inner_depend.get(procedure._name))
                file.writelines(str)

    def execute_singlefile(self, fileobj, target_dir= os.path.dirname(__file__)):
        print("------开始刷新%s目录下的%s" % (fileobj._file, fileobj._name))
        file_path = os.path.join(target_dir, os.path.split(fileobj._file)[-1])
        with open(fileobj._file, 'r', encoding='utf-8') as f1:
            content = f1.read()
            print("\t 读取文件内容成功，开始刷新脚本")
            # result = self.connect.qrysql(content)
            result = {'code':1 , 'val': 'OOOKKKK'}
            if result.get('code') == 0:
                print("\t %s刷新成功，返回:%s"%(fileobj._name, result.get('val')))
                with open(file_path+'_OK','w',encoding='utf-8') as f:
                    f.write(content)
                return True
            if result.get('code') != 0:
                print("\t ERROR---%s失败，%s"%(fileobj._name, result.get('val')))
                return False

    def execute_managerfile(self,manager_type = ['procedure','table'] ):
        if 'procedure' in manager_type:
            print('\n%s********************开始批量输入存储过程,共%s个********************' % (now_time(),len(self.manager.procedure)))
            for pro in self.manager.procedure:
                time.sleep(1)
                self.execute_singlefile(pro)
        if 'table' in manager_type:
            print('\n%s********************始批量输入建表语句，共%s个********************' % (now_time(),len(self.manager.table)))
            for tab in self.manager.table:
                self.execute_singlefile(tab)
        print('%s********************完成批量刷入********************' % (now_time()))


if __name__ == '__main__':

   a = Operator(r'D:\0.12.1-190108-to肖耀\test')
   a.make_prepare_list()
   a.execute_managerfile()