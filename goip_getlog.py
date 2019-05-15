#!/usr/bin/python

import requests
import functools
import time
import os
import logging
import re

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
dev = DevInfo("192.168.1.57", "80", "root", "123456")


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
def getlog_func(logdir, logpath):
    requests_addr = "http://" + dev.ip + logpath + "?command=&filename="
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    # 如果文件不存在则创建
    logfile = logdir + logpath
    if not os.path.exists(logfile):
        os.system(r'touch %s' % logfile)
    else:
        print("log file exist")

    if 200 == requests_code:
        with open(logfile, "wb") as code:
            code.write(requests_result.content)
    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


@try_fun
def system_filemgmt_reptile():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/system_filemgmt_en.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # logging.info(requests_result.text)

        filemgmt = re.findall("var strFiles = '(.*?)'", requests_result.text)
        logging.info(filemgmt)

        # 都出来是字符串，使用eval转换成字典
        filedata = eval(filemgmt[1])

        # 如果嵌套文件夹不存在，则创建
        logdir = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        if not os.path.isdir(logdir + "/opt/ejoin/var/log/"):
            os.makedirs(logdir + "/opt/ejoin/var/log/")

        if not os.path.isdir(logdir + "/tffs/var/"):
            os.makedirs(logdir+ "/tffs/var/")

        for logpath in filedata["data"]:
            # print(logurl[1])
            getlog_func(logdir, logpath[1])

        check.result = 1

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


while True:

    if check.time_out >= 30:  # 超过30次都检测不到模块，退出
        logging.info("time out stop")
        exit()

    if 0 == check.result:
        system_filemgmt_reptile()
    else:
        logging.info("get log ok")
        exit()

    time.sleep(2)
