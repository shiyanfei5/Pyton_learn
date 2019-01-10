#encoding:utf-8

import re
import chardet

def analyse(file_path):
    with open(file_path, 'r') as file:
        con = file.read()
        print(con)

def detect_utf8(file_name):
  with open(file_name, 'r') as f:
      result = chardet.detect(f.read())
      return result



class SqlTable:
    def __init__(self , file_path):
        pass

class SqlProcedure:
    def __init__(self):
        pass

path = unicode(r'D:\0.12.1-190108-to肖耀\0.12.1-190108-to肖耀\ELK更新\肖耀 - 备端\计算盈利买卖匹配的过程_完成.SQL','utf-8')
print detect_utf8(path)