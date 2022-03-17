#!/usr/bin/python3

import requests
import json
import os
import time
import logging
import functools


class CheckInfo(object):
    def __init__(self, result, count, start_time, use_time):
        self.count = count  # 测试次数
        self.start_time = start_time  # 测试起始时间
        self.use_time = use_time  # 测试用时

    time_out = 0


class DevInfo(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip  # 设备IP
        self.port = port  # 端口
        self.username = username  # 用户名
        self.password = password  # 密码


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
dev = DevInfo("192.168.1.232", "8080", "admin", "root123456")

cookie_str = ''

if False == os.path.exists("log"):
    print("log file don't exist.create.")
    os.major("log")
else:
    print("log file exist")

logging.basicConfig(#filename="log/goip_switch.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("#############################test start###########################")

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

def get_cookie_fun():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?op=get&sw_ver&username=" + dev.username + "&password=" + dev.password
    requests_resule = requests.get(requests_addr, timeout=(5, 5))
    requests.code = requests_resule.status_code
    print(requests_resule)

#    if 200 == requests_code:
#       logging.info("code:%d" % requests_resule.requests_code)
    result_dict = requests_resule.json()
    logging.info(result_dict)
    logging.info(requests_resule.headers)
    cookie_value = requests_resule.headers['Set-Cookie']
    logging.info("11:%s", cookie_value)
    global cookie_str
    cookie_str = cookie_value[0:44]
    logging.info(cookie_str)


get_cookie_fun()
@try_fun
def send_cmd_fun():
    global cookie_str
    httpmsg_cookies = cookie_str
    requests_addr = 'http://192.168.1.232:8080/goip_send_ussd.html?port=1&ussd=123'
    header_dict = {'Content-Type': 'application/json',
                   'Cookie': httpmsg_cookies,
                   'Host': '',
                   'Content-Length': '',
                   # 'Connection': 'Keep-alive',
                   # 'Origin': 'http://192.168.1.232',
                   # 'Referer': 'http://192.168.1.232/',
                   }
    logging.info(requests_addr)
    logging.info(header_dict)
    requests_result = requests.post(requests_addr, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)


    result_dict = requests_result.json()
    logging.info(result_dict)


send_cmd_fun()



