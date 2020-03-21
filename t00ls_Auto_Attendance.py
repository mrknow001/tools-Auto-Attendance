import hashlib
import requests
import re
import sys

with open('toolsuser.txt',mode='r+') as f:
    userinfo = f.read()
    
info = re.findall('[^\n].*',userinfo)

username = info[0]
passwd = info[1]
questionid = info[2]
answer = info[3]
login_url = "https://www.t00ls.net/logging.php?action=login&loginsubmit=yes&inajax=1"
Attendance_url = "https://www.t00ls.net/ajax-sign.json"

#print (username,passwd,questionid,answer)
def get_md5(data):
    obj = hashlib.md5()
    obj.update(data.encode('utf-8'))
    result = obj.hexdigest()
    return result

proxies = {
        "http":"http://127.0.0.1:8080",
        "https":"https://127.0.0.1:8080",
    }

pwd = get_md5(passwd)
#print (pwd)

def login(username,passwd,questionid,answer):

    headers = {"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    data = {'username':username,'password':pwd,'questionid':questionid,'answer':answer}
    response = requests.post(url=login_url,headers=headers,data=data,proxies=proxies,verify=False)

    cookie = requests.utils.dict_from_cookiejar(response.cookies)

    if not re.findall('.*'+username+'.*',response.text):
        print ('登陆失败')
        sys.exit()
    else:
        print ('登陆成功')
        return cookie


cookies = login(username,pwd,questionid,answer)

def Attendance(cookies):
    headers = {"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    data = {"formhash":"9dc3f214","signsubmit":"apply"}
    response = requests.post(url=Attendance_url,headers=headers,cookies = cookies,data=data,proxies=proxies,verify=False)
    with open('tools_index.html',mode='w+') as f:
        userinfo = f.write(response.text)

    if re.findall('{"status":"(fail|success)"',response.text):
        if re.findall('{"status":"(fail|success)"',response.text) == 'success':
            print ('签到完成')
        else:
            print ('签到失败')
    else:
        print ('签到出错')
        
Attendance(cookies)
