#!/usr/bin/python

import requests
import json
import os
import  logging
import functools

'''
class DevInfo(object)
    def __init__(self, ip, port, username, password):
        self.ip = ip    # 设备ip
        self.port = port    #设备端口
        self.username = username     #设备登录用户名
        self.password = password     #设备登录密码


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
dev = DevInfo ("192.168.1.58", "80", "root", "root")


if False == os.path.exists("log")
    print("log file not exist .create")
    os.mkdir("log")

else:
    print("log is exist")

logging.basicConfig(# filename ="log/sms receive failed log")  #指定输出的文件
            level=logging.DEBUG
            format = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging info("###############################test start###################################")

@try_fun
def goip_command_reptile():
    url = 'http://192.168.1.58:80/goip_post_sms.html?username=root&password=root'
    payload = {"type":"send-sms","task_num":1, "tasks":[{"tid":1223,"to":"10010","sms":"hello[]123"}]}
    headers = {'content-type': 'application/json,charset=utf-8'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)
         print(r.status_code)

        if r.status_code == 200:    #响应是200
            logging.info("code:%d" % r.status_code)
        else:
            r.status_code !== 200:      # 响应不是200
            logging.info("code:%d" % r.status_code)

    return requests.post
'''
    num = "test"
    print num





