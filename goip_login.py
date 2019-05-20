#!/usr/bin/python

import requests
import functools
import time
import os
import logging
import re
import hashlib
import json

if not os.path.exists("log"):
    print("log file don't exist.create")
    os.mkdir("log")
else:
    print("log file exist")


logging.basicConfig(#filename="log/goip_recovery.log", # 指定输出的文件
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("#######################test start#######################")


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
# dev = DevInfo("192.168.0.167", "80", "root", "root")
# dev = DevInfo("192.168.1.60", "80", "root", "root")
# dev = DevInfo("192.168.1.57", "80", "root", "123456")
dev = DevInfo("www.ejoinerm.com", "53458", "root", "root123")


def md5value(s):
    password = hashlib.md5()
    password.update(s.encode(encoding='utf-8'))
    print('password:', password.hexdigest())
    return password.hexdigest()

passwordmd5 = md5value('root:root123:c0a801340000099b5d7e44ec')
print('passwordmd5:',passwordmd5)

url = "http://www.ejoinerm.com:53458/login_en.html"
body = {}
headers = {'content-type':"application/x-www-form-urlencoded"}
response = requests.post(url, headers = headers)
print(response.text)

cookies_nonce = re.findall('var cookies_nonce = (.*?);', response.text)
print(cookies_nonce)