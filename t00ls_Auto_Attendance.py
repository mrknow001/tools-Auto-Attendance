# -*-coding:utf-8 -*-
import hashlib
import requests
import re
import sys
import os

def get_md5(data):
    obj = hashlib.md5()
    obj.update(data.encode('utf-8'))
    result = obj.hexdigest()
    return result
'''
proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"https://127.0.0.1:8080",
    }
'''
def login(username,passwd,questionid,answer):

    headers = {"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    data = {'username':username,'password':pwd,'questionid':questionid,'answer':answer}
#    response = requests.post(url=login_url,headers=headers,data=data,proxies=proxies,verify=False)
    response = requests.post(url=login_url,headers=headers,data=data)
    error = re.findall('密码错误次数过多，请 15 分钟后重新登录',response.text)
    
    cookie = requests.utils.dict_from_cookiejar(response.cookies)

    if not re.findall('.*'+username+'.*',response.text):
        print ('第'+str(i+1)+'个账号登陆失败，请检查用户名与密码')
        print (error[0])
        print ()
        return 1
    else:
        print ('登陆成功')
        return cookie

def Attendance(Att_ID):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With":"XMLHttpRequest",
               }
    data = {"formhash":Att_ID,"signsubmit":"apply"}
    #response = requests.post(url=Attendance_url,headers=headers,cookies = cookies,data=data,proxies=proxies,verify=False)
    response = requests.post(url=Attendance_url,headers=headers,cookies = cookies,data=data)
    with open('tools_index.html',mode='w+') as f:
        userinfo = f.write(response.text)

    if re.findall('{"status":"(fail|success)"',response.text):
#        print (re.findall('{"status":"(fail|success)"',response.text))
        if re.findall('{"status":"(fail|success)"',response.text)[0] == 'fail':
            print ('签到失败')
        else:
            print ('签到成功')
    else:
        print ('签到出错')
        
def Attendance_ID(cookies):
    headers = {"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}
    data = {'username':username,'password':pwd,'questionid':questionid,'answer':answer}
    #response = requests.post(url=get_ID_url,headers=headers,cookies=cookies,proxies=proxies,verify=False)
    response = requests.post(url=get_ID_url,headers=headers,cookies=cookies)
    uid = re.findall('discuz_uid\s+=\s+(\d+)',response.text)
    url = 'https://www.t00ls.net/members-profile-'+uid[0]+'.html'
    #response_2 = requests.get(url=url,headers=headers,cookies=cookies,proxies=proxies,verify=False)
    response_2 = requests.get(url=url,headers=headers,cookies=cookies)
    if re.findall('value="已签到 \(\d天\)"',response_2.text):
        return 0
    else:
        Att_ID = re.findall('javascript:WebSign\(\'(.*)?\'\)',response_2.text)
        if not Att_ID[0]:
            print ('未获取到签到ID')
            return
        else:
            return Att_ID[0]


if __name__ == '__main__':

    login_url = "https://www.t00ls.net/logging.php?action=login&loginsubmit=yes&inajax=1"
    Attendance_url = "https://www.t00ls.net/ajax-sign.json"
    get_ID_url = 'https://www.t00ls.net/memcp.php'

    isfile  = os.path.isfile('toolsuser.txt')
    if not isfile:
        fp = open("toolsuser.txt",mode='w')
        fp.close()
        print ('文件不存在')
        print ('toolsuser.txt创建完成，请在文本中输入账号信息')
    
    with open('toolsuser.txt',mode='r+',encoding='utf-8') as f:
        userinfo = f.read()
    
    info = re.findall('[^\n].*',userinfo)
    
    length = len(info)

    if length < 4:
        print ('文本中没有账号信息,请在toolsuser.txt文本在输入账号、密码、第几个问题、回答，每一项一行，如果有多个账号往下填')
        sys.exit()
    a = int(length/4)
    for i in range(a):
        username = info[0+i*4]
        passwd = info[1+i*4]
        questionid = info[2+i*4]
        answer = info[3+i*4]

        pwd = get_md5(passwd)
        cookies = login(username,pwd,questionid,answer)
        if cookies == 1:
            continue
        Att_ID = Attendance_ID(cookies)
        if Att_ID == 0:
            print ('此账号已经签到')
            continue
        Attendance(Att_ID)

