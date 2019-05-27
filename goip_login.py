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

'''
class CheckInfo(object):
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
dev = DevInfo("192.168.1.57", "80", "root", "123456")
'''
url = "http://192.168.1.60/login_en.html"
body = {}
headers = {'content-type':"application/x-www-form-urlencoded"}
response = requests.post(url, headers = headers)
#print(response.text)

cookies_nonce = re.findall('var cookies_nonce = "(.*?)";', response.text)
print(cookies_nonce[0])

def md5value(s):
    password = hashlib.md5()
    password.update(s.encode(encoding='utf-8'))
    print('password:', password.hexdigest())
    return password.hexdigest()

s = "root:" + "root123:" + cookies_nonce[0]
passwordmd5 = md5value(s)


url = "http://192.168.1.60/login_en.html"
encoded_value ="root:"+ passwordmd5
params = {"nonce":"",
        "encoded":encoded_value,
        "loginStatus":""
         }
#http请求头
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Host":"192.168.1.60",
    "Referer":"http://192.168.1.60/login_en.html",
    "cookie":"cookies_nonce",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
response = requests.post(url,data=params)
#print(response.text)

loginStatus = re.findall('id="ID_LoginStatus" name="loginStatus" value="(.*?)"',response.text)
print(loginStatus[0])
'''
#发送get请求获取post_status页面
url = "http://192.168.1.60/port_status_en.html"
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "cookie": "cookies_nonce;username=5",
    "Host":"192.168.1.60",
    "Referer":"http://192.168.1.60/main_left_en.html",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
response = requests.get(url)
print(response.text)
'''

def recovery_fun():
    # 绑定浏览器
    Browser = webdriver.Chrome()
    # 最大化浏览器
    Browser.maximize_window()
    # 打开页面
    url = "http://" + dev.ip + "/login_en.html"
    Browser.get(url)

    # 用户名的定位
    Browser.find_element_by_id("accountID").clear()
    Browser.find_element_by_id("accountID").send_keys(dev.username)
    time.sleep(1)
    # 密码的定位
    Browser.find_element_by_id("passwordID").clear()
    Browser.find_element_by_id("passwordID").send_keys(dev.password)
    time.sleep(1)
    # 点击登录
    Browser.find_element_by_id("btnLoginID").click()
    time.sleep(1)
    # 判断弹出内容，并处理
    result = expected_conditions.alert_is_present()(Browser)
    if result:
        result = Browser.switch_to.alert
        print(result.text)
        if "用户名或密码错误" in result.text:
            print("密码错误,停止测试")
            exit()
        else:
            result.accept()
    else:
        print("alert 未弹出")
    Browser.switch_to.frame(0)
    # 切换到左侧frame
    Browser.switch_to.frame("left")

