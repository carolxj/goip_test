#!/usr/bin/python

import requests
import functools
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
import re
import json
import io
if False == os.path.exists("log"):
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
dev = DevInfo("192.168.1.51", "80", "root", "root")
#dev = DevInfo("192.168.1.159", "80", "root", "123456")
# dev = DevInfo("192.168.1.60", "80", "root", "root")
# dev = DevInfo("192.168.1.54", "80", "root", "root")


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
def port_status_reptile():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/port_status_en.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        #logging.info(requests_result.text)

        port_status = re.findall("strPortStatus = '(.*?)'", requests_result.text)
        # logging.info(port_status)
        # findall返回的是list，取list的第一个元素转换成字典
        port_dict = json.loads(port_status[0])
        # logging.info(port_dict)
        max_ports = port_dict["count"]
        logging.info(max_ports)

        # 读取每个端口的状态，并判断是否存在
        modem_status = {}
        check_ng = 0
        for i in range(max_ports):
            modem_status[i] = port_dict["data"][i][3]
            # 判断模块是否都存在，只要有一个不存在则置标志位
            if 'No' == modem_status[i]:
                check_ng = 1
                logging.info("modem %d ng,result:%s" % (i + 1, modem_status[i]))

        if 0 == check_ng:
            logging.info("check_result ok")
            check.result = 1
            check.time_out = 0  # 超时清零
        else:
            logging.info("check_result ng count: %d" % check.time_out)
            check.result = 0
            check.time_out += 1  # 超时加1

        logging.info(modem_status)

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


# def recovery_fun():
#     # 绑定浏览器
#     Browser = webdriver.Chrome()
#     # 最大化浏览器
#     Browser.maximize_window()
#     # 打开页面
#     url = "http://" + dev.ip + "/login_en.html"
#     Browser.get(url)
#
#     # 用户名的定位
#     Browser.find_element_by_id("accountID").clear()
#     Browser.find_element_by_id("accountID").send_keys(dev.username)
#     time.sleep(1)
#     # 密码的定位
#     Browser.find_element_by_id("passwordID").clear()
#     Browser.find_element_by_id("passwordID").send_keys(dev.password)
#     time.sleep(1)
#     # 点击登录
#     Browser.find_element_by_id("btnLoginID").click()
#     time.sleep(1)
#     # 判断弹出内容，并处理
#     result = expected_conditions.alert_is_present()(Browser)
#     if result:
#         result = Browser.switch_to.alert
#         print(result.text)
#         if "用户名或密码错误" in result.text:
#             print("密码错误,停止测试")
#             exit()
#         else:
#             result.accept()
#     else:
#         print("alert 未弹出")
#     Browser.switch_to.frame(0)
#     # 切换到左侧frame
#     Browser.switch_to.frame("left")
#     # 点击保存重启/html/body/div[9]/div/a     /html/body/div[9]/div/a/span
#     Browser.find_element_by_xpath("/html/body/div[9]/div/a").click()
#     # 点击系统升级或恢复/html/body/div[7]/div[2]/ul/li[6]/a
#     #Browser.find_element_by_xpath('//*[@id="M7"]/ul/li[6]/a/span').click()
#     # 返回主页，重新选择frame(不知道为什么要这样做)
#     Browser.switch_to.default_content()
#     Browser.switch_to.frame(0)
#     # # 切换到右侧frame
#     Browser.switch_to.frame("right")
#     # 点击重启按钮
#     Browser.find_element_by_id("ID_BtnReboot").click()
#     time.sleep(1)
#     # 判断弹出内容，并处理
#     result = expected_conditions.alert_is_present()(Browser)
#     if result:
#         result = Browser.switch_to.alert
#         print(result.text)
#         if "确定重启网关吗?" or "Are you sure to reboot the gateway?" in result.text:
#             result.accept()
#     else:
#         print("alert 未弹出")
#
#     time.sleep(2)
#     # 关闭浏览器
    Browser.quit()

    logging.info("all modem check ok,recovery")
    check.result = 0

    check.use_time = time.time() - check.start_time
    logging.info("Num: %d ,use time:%s" % (check.count, check.use_time))
    check.count += 1

#   time.sleep(10)  # 重启需要一定的时间，延时后再开始下一次测试

    check.start_time = time.time()


while True:

    if check.time_out >= 30:  # 超过30次都检测不到模块，退出
        logging.info("time out stop")
        exit()

    if 0 == check.result:
        port_status_reptile()
    else:
        # recovery dev
        recovery_fun()

    time.sleep(2)
