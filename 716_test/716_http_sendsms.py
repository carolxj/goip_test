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


# 当服务器连不上，request会报错，所以需要加一个重试机制
@try_fun
# def get_cookie_fun():
#
#     requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?op=get&sw_ver&username=" + dev.username + "&password=" + dev.password
#     requests_result = requests.get(requests_addr, timeout=(5, 5))
#     requests_code = requests_result.status_code
#     print(requests_result)
#
#     if 200 == requests_code:
#         logging.info("code:%d" % requests_result.status_code)
#         # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
#         result_dict = requests_result.json()
#         logging.info(result_dict)
#         logging.info(requests_result.headers)
#         #获取cookie
#         cookie_value = requests_result.headers["Set-Cookie"]
#         logging.info("111:%s", cookie_value)
#         global cookie_str
#         cookie_str = cookie_value[0:44]
#         logging.info(cookie_str)
#
# get_cookie_fun()

@try_fun
def send_sms_fun():
    global cookie_str
    httpmsg_cookies = cookie_str
    logging.info(cookie_str)
    logging.info(httpmsg_cookies)
    requests_addr = 'http://192.168.1.58/goip_post_sms.html?username=root&password=root'
    data = {"type": "send-sms", "task_num": 1, "tasks": [{"tid": 1, "to": "16179522629", "sms": "Look at this tag of you"
    " Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 2, "to": "16179522629", "sms": "Look"
    " at this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 3, "to": "16179522629",
   "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 4, "to":
    "16179522629", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},
    {"tid": 5, "to": "16179522629", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
    ".com/VhDvZBgh"},{"tid": 6, "to": "16179522629", "sms": "Look at this tag of you Judy Garland posted without "
    "permission watchthelanguage.com/VhDvZBgh"},{"tid": 7, "to": "16179522629", "sms": "Look at this tag of you Judy "
    "Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 8, "to": "16179522629", "sms": "Look at"
    " this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 9, "to": "16179522629",
    "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},{"tid": 10, "to":
    "16179522629", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage.com/VhDvZBgh"},
    {"tid": 11, "to": "16179522629", "sms": "Look at this tag of you Judy Garland posted without permission watchthelanguage"
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
       code = requests_result.status_code
       logging.info(code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
       result_dict = requests_result.json()
       logging.info(result_dict)
       # logging.info(requests_result.headers)

    return code
code = send_sms_fun()

while True:
    if code == 200:
        send_sms_fun()

    time.sleep(1)


