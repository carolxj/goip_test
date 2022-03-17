#!/usr/bin/python3

import requests
import json
import os
import time
import logging
import functools


class CheckInfo(object):
    def __init__(self, result, count, start_time, use_time):
        self.result = result  #
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
dev = DevInfo("192.168.1.51", "8080", "admin", "admin")

if False == os.path.exists("log"):
    print("log file don't exist.create.")
    os.major("log")
else:
    print("log file exist")

logging.basicConfig(  # filename="log/goip_switch.log",
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


# 获取到cookie得时候就返回True,没有获取到得时候就返回False
@try_fun
def get_cookie_fun():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_get_status.html?username=" + dev.username + "&password=" + dev.password
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)

    result = True
    if 200 == requests_code:
        logging.info("code:%d" % requests_result.status_code)

        result_dict = requests_result.json()
        cookie_value = requests_result.headers['Set-Cookie']
        #    logging.info("11:%s", cookie_value)
        dev.cookie_str = cookie_value[0:44]
        logging.info(dev.cookie_str)

        return True
    else:
        logging.info("code:%s", requests_code)
        return False


@try_fun
def dev_redial_fun():
    httpmsg_cookies = dev.cookie_str
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.ht" \
                                                          "ml?&op=redial&port=1"
    header_dict = {'Content-Type': 'application/json',
                   'Cookie': httpmsg_cookies,
                   'Host': '',
                   'Content-Length': '',
                   # 'Connection': 'Keep-alive',
                   # 'Origin': 'http://192.168.1.59',
                   # 'Referer': 'http://192.168.1.59/',
                   }
    logging.info(requests_addr)
    logging.info(header_dict)
    requests_result = requests.get(requests_addr, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)

    result_dict = requests_result.json()
    logging.info(result_dict)

    result = True
    if 200 == requests_code:
        logging.info("redial OK")
        '''check.result = 0

        check.use_time = time.time() - check.start_time
        logging.info("Num: %d ,use time:%s" % (check.count, check.use_time))
        check.count += 1

        time.sleep(2)

        check.start_time = time.time()'''
        return True
    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)
        return False


@try_fun
def get_status_fun():

    #while是循环的入口，5次没成功则退出
    get_status_count = 0 # 定义次数；
    while True:
        logging.info("get_status_count:%d", get_status_count)
        if 5 == get_status_count:
            logging.info("test fail:%d", get_status_count)
            exit()
        else:
            get_status_count = get_status_count + 1
            time.sleep(5)

        httpmsg_cookies = dev.cookie_str
        requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?op=get&port_status&username=" \
                    + dev.username + "&password=" + dev.password
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
        if 200 == requests_code:

            logging.info("code:%d" % requests_result.status_code)
            # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
            result_dict = requests_result.json()
            logging.info(result_dict)

            #  for sim_status in sim_status:
            #获取卡的状态值
            sim_status = result_dict["data"]["port_status"][0]
            #logging.info("sim_status:%d" % sim_status)
            #如果卡的状态值不等于15，再执行一次获取卡状态，如果卡状态=15，返回turn，我刚才忙别的
            if 15 == sim_status:
                logging.info("sim_status:%d" %  sim_status)
                return True
            else:
                logging.info("sim_status:%d" % sim_status)


@try_fun
def dev_publicip_fun():
    httpmsg_cookies = dev.cookie_str
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?&op=get&port_public_ip&username=" + dev.username + "&password=" + dev.password
    header_dict = {'Content-Type': 'application/json',
                   'Host': '',
                   'Content-Length': '',
                   # 'Connection': 'Keep-alive',
                   # 'Origin': 'http://192.168.1.59',
                   # 'Referer': 'http://192.168.1.59/',
                   }
    logging.info(requests_addr)
    logging.info(header_dict)
    requests_result = requests.get(requests_addr, headers=header_dict, timeout=(5, 5))
    requests_code = requests_result.status_code
    print(requests_result)

    result_dict = requests_result.json()
    logging.info(result_dict)

    public_ip = result_dict["data"]["port_public_ip"][0]
    logging.info("public_ip:%s" % public_ip)

    if 200 == requests_code:
        #logging.info("sim")
        check.result = 0

        check.use_time = time.time() - check.start_time
        logging.info("Num: %d ,use time:%s" % (check.count, check.use_time))
        check.count += 1

        time.sleep(10)  # 重启需要一定的时间，延时后再开始下一次次测试
        check.start_time = time.time()
    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)
        return True

        result = True  # 默认所有模块都正常

        if result == False:
            return False
        else:
            return True


while True:
    if check.time_out >= 100:  # 超过30次都检测不到模块，退出
        exit()

    if False == get_cookie_fun():  # 先get cookie,失败退出，成功执行重拨
        exit()
    else:
        redial = dev_redial_fun()
        if True == redial:
            time.sleep(10)
            status = get_status_fun()

            if True == status:
                dev_publicip_fun()
                time.sleep(60)


