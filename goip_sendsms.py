#!/usr/bin/python3

import requests
import os
import logging
import time
import functools
import json
import re

class CheckInfo(object):
    def __init__(self, result, count, start_time, use_time):
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
dev = DevInfo("192.168.1.58", "80", "root", "root")

cookie_str = ''

if False == os.path.exists("log"):
    print("log file don't exist.create")
    os.mkdir("log")
else:
    print("log file exist")

logging.basicConfig(#filename="log/goip_switch.log", # 指定输出的文件
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("#######################test start#######################")


def try_fun(func):
    if callable(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:  # 进行异常捕获
                response = func(*args, **kw)
            except Exception as e:
                print(e)
                response = None
            return response
        return wrapper
    else:
        def decorator(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kw):
                try:  # 进行异常捕获
                    response = fn(*args, **kw)
                except Exception as e:
                    print(e)
                    response = None
                return response
            return wrapper
        return decorator

@try_fun
def send_sms_fun():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_post_sms.html?username=" + dev.username + "&password=" + dev.password
    data = {"type": "send-sms", "task_num": 10, "tasks": [{"tid": 12, "to": "16179522629", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 13, "to": "16178778716", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 14, "to": "17074188143", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 15, "to": "15094212018", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 16, "to": "15094212018", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 17, "to": "19036190556", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 18, "to": "18703104891", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 19, "to": "16158642601", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 1, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 2, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 3, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 4, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 5, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 6, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 7, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 8, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 9, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 10, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 11, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 12, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 20, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 21, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 22, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 23, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 24, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 25, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 26, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 27, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 28, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 29, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 30, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 31, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 32, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 33, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 34, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 35, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 36, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 37, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 38, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 39, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 40, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 41, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 42, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 43, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 44, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 45, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 46, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 47, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 48, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 49, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 50, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 51, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 52, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 53, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 54, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 55, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 56, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 57, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 58, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 59, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 60, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 61, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 62, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 63, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 64, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 65, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 66, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 67, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 68, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 69, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 70, "to": "17196591792", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"}]}
    body = json.dumps(data)
    header_dict = {'Content-Type': 'application/json',
                   'Host': '',
                   'Content-Length': '',
                   # 'Connection': 'Keep-alive',
                   # 'Origin': 'http://192.168.1.58',
                   # 'Referer': 'http://192.168.1.58/',
    }
    logging.info(requests_addr)
    logging.info(body)
    logging.info(header_dict)
    requests_result = requests.post(requests_addr, data=body, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)

    if 200 == requests_code:
       logging.info("code:%d" % requests_result.status_code)
       # code = requests_result.status_code
       # logging.info(code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
       result_dict = requests_result.json()
       logging.info(result_dict)
       # logging.info(requests_result.headers)

    return requests_code
code = send_sms_fun()

while True:
    if code == 200:
        send_sms_fun()

    time.sleep(0.5)


