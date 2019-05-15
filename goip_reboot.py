#!/usr/bin/python

import requests
import os
import logging
import time
from retrying import retry


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
# dev = DevInfo("192.168.1.159", "80", "root", "123456")
# dev = DevInfo("192.168.1.54", "80", "root", "root")
dev = DevInfo("192.168.1.54", "80", "root", "root")


if False == os.path.exists("log"):
    print("log file don't exist.create")
    os.mkdir("log")
else:
    print("log file exist")

logging.basicConfig(#filename="log/goip_reboot.log", # 指定输出的文件
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

logging.info("#######################test start#######################")


# 当服务器连不上，request会报错，所以需要加一个重试机制，最大重试3次，3次全部报错，才会报错
@retry(stop_max_attempt_number=3)
def _modem_check_fun():

    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_get_status.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout = (5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
        result_dict = requests_result.json()
        logging.info(result_dict)

        # 获取总端口数
        max_ports = result_dict["max-ports"]

        # 读取每个端口的IMEI，并判断是否存在
        modem_status = {}
        check_ng = 0
        for i in range(max_ports):
            modem_status[i] = result_dict["status"][i]["imei"]
            # 判断模块是否都存在，只要有一个不存在则置标志位
            if '' == modem_status[i]:
                check_ng = 1

        if 0 == check_ng:
            logging.info("check_result ok")
            check.result = 1
            check.time_out = 0   # 超时清零
        else:
            logging.info("check_result ng count: %d"% check.time_out)
            check.result = 0
            check.time_out += 1  # 超时加1

        logging.info(modem_status)

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


# 模块检测函数
def modem_check_fun():
    try:  # 进行异常捕获
        response = _modem_check_fun()
    except Exception as e:
        print(e)
        response = None
    return response


# 当服务器连不上，request会报错，所以需要加一个重试机制，最大重试3次，3次全部报错，才会报错
@retry(stop_max_attempt_number=3)
def _dev_reboot_fun():

    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?username=" + dev.username + "&password=" + dev.password + "&op=reboot"
    requests_result = requests.get(requests_addr)
    requests_code = requests_result.status_code

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

    return requests_result


# 设备重启函数
def dev_reboot_fun():
    try:  # 进行异常捕获
        response = _dev_reboot_fun()
    except Exception as e:
        print(e)
        response = None
    return response


while True:

    if check.time_out >= 30:  # 超过30次都检测不到模块，退出
        exit()

    if 0 == check.result:
        modem_check_fun()
    else:
        # reboot dev
        dev_reboot_fun()

    time.sleep(2)

