#!/usr/bin/python3

import requests
import json
import os
import time
import logging
import functools


class CheckInfo(object):
    def __init__(self, result, count, start_time, use_time):
        self.result = result #
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

    cookie_str = ''


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
dev = DevInfo("192.168.1.58", "8080", "root", "root")


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

#获取到cookie得时候就返回True,没有获取到得时候就返回False
@try_fun
def get_cookie_fun():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?op=get&sw_ver&username=" + dev.username + "&password=" + dev.password
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code
#    print(requests_resule)

    result = True
    if 200 == requests_code:
        logging.info("code:%d" % requests_result.status_code)

        result_dict = requests_result.json()
        # result_dict = requests_resule.text
        logging.info(result_dict)
        logging.info(requests_result.headers)
        cookie_value = requests_result.headers['Set-Cookie']
        #    logging.info("11:%s", cookie_value)
        dev.cookie_str = cookie_value[0:44]
        logging.info(dev.cookie_str)

        return True
    else:
        logging.info("code:%s", requests_code)
        return False


@try_fun
def get_status_fun():
    httpmsg_cookies = dev.cookie_str
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_get_status.html"
    header_dict = {'Content-Type': 'application/json',
                   'Cookie': httpmsg_cookies,
                   'Host': '',
                   'Content-Length': '',
                   }
    logging.info(requests_addr)
    logging.info(header_dict)
    requests_result = requests.get(requests_addr, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)

    result_dict = requests_result.json()

    if 200 == requests_code:
        logging.info("code:%d" % requests_result.status_code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
        result_dict = requests_result.json()
        logging.info(result_dict)

        # 获取总端口数
        max_ports = result_dict["max-ports"]
        logging.info(max_ports)
        # 读取每个端口的IMEI，并判断是否存在
        modem_status = {}
        check_ng = 0
        result = True #默认所有模块都正常
        for i in range(max_ports):
            modem_iccid = None
            modem_iccid = result_dict["status"][i]["iccid"]
            logging.info(modem_imei)
            #这边要判断imei是否存在,有一个不存在就返回错误,
            if None == modem_iccid:
                result = False #有一个模块出问题得时候就会被设置成False

        if result == False:
            return False
        else:
            return True


@try_fun
def dev_reboot_fun():
    httpmsg_cookies = dev.cookie_str
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?op=reboot"
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
    requests_result = requests.get(requests_addr, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)


    result_dict = requests_result.json()
    logging.info(result_dict)

    if 200 == requests_code:
        logging.info("all modem check ok,reboot")
        check.result = 0

        check.use_time = time.time() - check.start_time
        logging.info("Num: %d ,use time:%s" % (check.count, check.use_time))
        check.count += 1

        time.sleep(10)       # 重启需要一定的时间，延时后再开始下一次次测试

        check.start_time = time.time()
    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)




while True:
    if check.time_out >= 100:  # 超过30次都检测不到模块，退出
        exit()

    if False == get_cookie_fun():  # 先get cookie,
        exit()

    if True == get_status_fun():
        dev_reboot_fun()

        time.sleep(60)


    

        


