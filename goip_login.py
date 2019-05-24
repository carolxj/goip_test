#!/usr/bin/python

import requests
import functools
import time
import os
import logging
import re
import hashlib
import json
import sys
import io
import urllib.request
import http.cookiejar

if not os.path.exists("log"):
    print("log file don't exist.create")
    os.mkdir("log")
else:
    print("log file exist")


logging.basicConfig(#filename="log/goip_recovery.log", # 指定输出的文件
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("#######################test start#######################")


'''class CheckInfo(object):
    def __init__(self, result, count, start_time, use_time):
        self.result = result  # 判断模块是否检测完成，0-未完成，1-完成
        self.count = count    # 测试次数
        self.start_time = start_time  # 测试起始时间
        self.use_time = use_time  # 测试用时

    time_out = 0


class DevInfo(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip    # 设备IP
        self.port = port  # 设备端口
        self.username = username  # 用户名
        self.password = password  # 密码


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
# dev = DevInfo("192.168.0.167", "80", "root", "root")
# dev = DevInfo("192.168.1.60", "80", "root", "root")
# dev = DevInfo("192.168.1.57", "80", "root", "123456")'''

url = "http://192.168.1.58/login_en.html"
body = {}
headers = {'content-type':"application/x-www-form-urlencoded"}
response = requests.post(url, headers = headers)
#print(response.text)

cookies_nonce = re.findall('var cookies_nonce = "(.*?)";', response.text)
print(cookies_nonce)

def md5value(s):
    password = hashlib.md5()
    password.update(s.encode(encoding='utf-8'))
    #print('password:', password.hexdigest())
    return password.hexdigest()

passwordmd5 = md5value('root:root123:cookies_nonce')
print(passwordmd5)

'''url = "http://192.168.1.58/login_en.html"
encoded_value ="root:"+passwordmd5
params = {"encoded":encoded_value}
response = requests.post(url,data=params)
#print(response.text)

loginStatus = re.findall('id="ID_LoginStatus" name="loginStatus" value="(.*?)"',response.text)
print(loginStatus)

#http请求头
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Host":"192.168.1.58",
    "Referer":"http://192.168.1.58/login_en.html",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

'''

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#登录时需要提交的表单
encoded_value ="root:"+passwordmd5
params = {"encoded":encoded_value}

#设置请求头
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#登录时表单提交到的url
login_url = 'http://192.168.1.58/login_en.html'

#登录请求
requests = urllib.request.Request(login_url,headers = headers,data = params)
#构造cookie
cookie = http.cookiejar.CookieJar()
#由cookie构造opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
#发送登录请求
resp = opener.open(requests)

#登录后才能访问的页面
url = ''





