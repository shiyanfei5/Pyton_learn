#encoding:utf-8
import os

def _check_filetype(file, type=['SQL']):
    '''
    type的内容请大写，用于检查文件类型
    '''
    filename = os.path.split(file)[-1]
    file_type = str(filename).split('.')[-1]
    if  file_type.upper() in type:
        return True
    return False

def find_files(dir_path, file_check = _check_filetype):
    """
    迭代查找path目录下的所有sql文件目录，最终返回数据结构如下..广度优先
    ['文件1','文件2','文件3']
    file_check为一个可调用对象，用于判断file
    """
    if os.path.isdir(dir_path):
        # 获得当前目录所有文件夹
        cur_dir = []    # 广度优先文件夹
        cur_file = []
        for item in os.listdir(dir_path):
            item = os.path.join(dir_path , item)
            if os.path.isdir(item):
                cur_dir.append(item)
            else:
                if callable(file_check):
                    if file_check(item):
                        cur_file.append(item)
                else:
                    cur_file.append(item)

        for call in cur_dir:
            result = find_files( call,file_check )
            cur_file.extend(result)
        return cur_file
    else:
        return  [] # 若为文件返回为空



if __name__ == '__main__':
    path = r'D:\python_project\db_deploy\0.12.1-190108-to肖耀'

    a = find_files(path,_check_filetype)
    for i in a:
        print(i)

