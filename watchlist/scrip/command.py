import requests
import json
url = 'http://43.133.11.104'
def getuserstatu(uid):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {}
    re = requests.get(url + '/userstatus' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def getuser(uid):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {}
    re = requests.get(url + '/user' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False
a = getuser(1)
print('d')
def rootset(uid,lever,fengxian):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'lever': lever, 'fengxian': fengxian}
    re = requests.post(url + '/rootset' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def adduser(uid,user):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'userid': user.id, 'name': user.name, 'username': user.username}
    re = requests.post(url + '/adduser' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def deluser(uid,delid):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'delid': delid}
    re = requests.post(url + '/deluser' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def getorder(uid, year, month=None, day=None):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'year': year, 'month': month, 'day': day}
    re = requests.get(url + '/order' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def gettotalfig(uid, year, month, day=None):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'year': year, 'month': month, 'day': day}
    re = requests.get(url + '/totalfig' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)['message']
        return True, info
    return False

def setapikey(uid, apikey, secretkey, pt=None):
    if not isinstance(uid, str):
        uid = str(uid)
    params = {'apikey': apikey, 'secretkey': secretkey, 'pt': pt}
    re = requests.post(url + '/setkey' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False

def setrun(uid):
    if not isinstance(uid, str):
        uid = str(uid)
    params = None
    re = requests.post(url + '/setkey' + uid, params=params)
    if re.status_code == 200:
        info = json.loads(re.text)
        if info['code'] == 1:
            return True, info['message']
        return False, info['message']
    return False, '网络连接失败'

def to_dict(objj):
    is_list = objj.__class__ == [].__class__
    is_set = objj.__class__ == set().__class__
    x = 0
    if is_list or is_set:
        obj_arr = {}
        for o in objj:
            # 把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr[x] = dict
            x = x + 1
        return obj_arr
    else:
        print('2')
        dict = {}
        dict.update(objj.__dict__)
        return dict

