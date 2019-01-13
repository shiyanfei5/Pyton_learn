
import requests
import json
import os

ELK_MAIN = {
    'username':'',
    'password':'',
    'login_url':'',
    'signature':'',
    'role':''
}

class ElkQuery:
    """
    调用大数据接口进行查询
    """
    def __init__(self, ELK_CONFIG ):

        _username = ELK_CONFIG.get('username')
        _password = ELK_CONFIG.get('password')
        _login_url = ELK_CONFIG.get('login_url')
        _signature = ELK_CONFIG.get('signature')
        _role = ELK_CONFIG.get('role')
        _log_params = json.dumps({'username':_username,'password':_password})
        _res =  requests.post(_login_url, _log_params)
        _token = _res.headers.get('Authorization')
        self._base_url = ELK_CONFIG.get('base_url')
        self._headers = {'Authorization':_token,'signature':_signature,'role':_role,'USERNAME':_username,'content-type':'application/json'}

    # 宏存储过程
    def savemac(self,sql,sqlid,resultFlag='N'):
        savemac_url = self._base_url + "/base-service/ddl/savemac"
        rst = requests.post(savemac_url, json.dumps({'sql':sql,'sqlId':sqlid,'resultFlag':resultFlag}), headers=self._headers)
        if rst.json().get('msg') == '请求成功':
            return rst.json()
        else:
            return rst.json().get('msg')

    # 宏执行过程
    def execmac(self,sqlid, value,kvflag=None):
        execmac_url = self._base_url + "/base-service/ddl/execmac"
        params =  {'execParams':{sqlid:value}, 'kvflag':kvflag}
        rst = requests.post(execmac_url, json.dumps(params), headers=self._headers)
        if rst.json().get('msg') == '请求成功':
            return 1
        else:
            return rst.json().get('msg')

    # 存储过程执行
    def execcall(self,sqls):
        execcall_url = self._base_url + "/base-service/ddl/call"
        rst = requests.post(execcall_url, json.dumps({'sqls': sqls}), headers = self._headers)
        if rst.json().get('code') == 0:
            return 1
        else:
            return rst.json()

    # sql查询过程
    def qrysql(self,sqls,kvflag=None):
        qrysql_url = self._base_url + "/base-service/ddl/query"
        rst = requests.post(qrysql_url, json.dumps({'sqls':sqls, 'kvflag':kvflag}), headers = self._headers)

        if rst.json().get('code') != 0:
            return {"code":400, "val":rst.json().get('msg')}
        else:
            return {"code":0, "val":rst.json()['result']}

    # sql更新过程
    def updsql(self, sqls):
        update_url = self._base_url + "/base-service/ddl/update"
        rst = requests.post(update_url, json.dumps({'sqls':sqls,'kvflag':None}), headers = self._headers)
        if rst.json().get('code') == 0:
            return 1
        else:
            return rst.json().get('msg')

    # 宏删除过程
    def delmac(self,sqlid):
        delmac_url = self._base_url + "/base-service/ddl/delmac"
        rst = requests.post(delmac_url, json.dumps({'sqlId':sqlid}), headers = self._headers)
        if rst.json().get('code') == 0:
            return 1
        else:
            return rst.json().get('msg')
