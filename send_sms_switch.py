#!/usr/bin/python

import requests
import json
import os
import logging
import functools
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
import re
import json

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
    test_step = 0


class DevInfo(object):
    def __init__(self, ip, port, username, password):
        self.ip = ip    # 设备IP
        self.port = port  # 设备端口
        self.username = username  # 用户名
        self.password = password  # 密码


class SimInfo(object):
    def __init__(self, port, slot, phone):
        self.port = port     # 插在设备那个端口
        self.slot = slot     # 插在设备端口的哪个卡槽，A/B/C/D
        self.phone = phone   # 电话号码


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
check.test_step = 0
check.result = 0
dev = DevInfo("192.168.1.51", "80", "root", "test123")
# dev = DevInfo("192.168.1.159", "80", "root", "123456")
# dev = DevInfo("192.168.1.60", "80", "root", "root")
# dev = DevInfo("192.168.1.54", "80", "root", "root")
sim1 = SimInfo(3, "A", "11111111111")  # 要发送短信的sim卡
sim2 = SimInfo(2, "B", "13509644850")  # 要接收短信的sim卡


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


# 切卡
@try_fun
def switch_sim_fun(modemid, simid):
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_send_cmd.html?username=" + dev.username + "&password=" + dev.password + "&op=switch" + "&ports=" + str(modemid) + "." + simid
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
        result_dict = requests_result.json()
        logging.info(result_dict)

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


# 获取当前卡所在位置
# modemid: 1-max_ports
@try_fun
def goip_switch_sim():

    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_get_status.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # 直接得出字典结构结果，或使用json.loads进行转换一次也行result_dict = json.loads(requests_result.content.decode())
        result_dict = requests_result.json()
        logging.info(result_dict)

        # 获取总端口数
        max_ports = result_dict["max-ports"]

        if (sim2.port > max_ports) or (sim2.port <= 0):
            logging.info("modemid:%d" % sim2.port)
            return "error"

        # 获取现在模块使用那个port的卡
        sim_id = result_dict["status"][sim2.port - 1]["port"]
        logging.info("sim_id:%s" % sim_id)
        sim_id = sim_id[3:4]  # 截取第二位

        if sim_id == "1":
            switch_sim_fun(sim2.port, "02")
        elif sim_id == "2":
            switch_sim_fun(sim2.port, "03")
        elif sim_id == "3":
            switch_sim_fun(sim2.port, "04")
        else:
            switch_sim_fun(sim2.port, "01")


    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


@try_fun
def goip_sms_stat_reptile():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_sms_stat_en.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # logging.info(requests_result.text)

        port_status = re.findall("strSmsStatList = '(.*?)'", requests_result.text)
        logging.info(port_status)
        # findall返回的是list，取list的第一个元素转换成字典
        port_dict = json.loads(port_status[0])
        logging.info(port_dict)
        max_ports = port_dict["count"]
        logging.info(max_ports)

        # 读取portId的短信发送状态，判断是否发送成功
        req_status = port_dict["data"][sim1.port][4]
        logging.info("req_status:%s, send_count:%s" % (req_status, check.count))
        # 判断模块是否都存在，只要有一个不存在则置标志位
        if check.count == req_status:
            logging.info("status ok")
            check.test_step = 4  # 设置到下一个阶段，切卡
            check.time_out = 0
        else:
            check.time_out += 1
            logging.info("status ng,time_out:%s" % check.time_out)

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


# 通过portId发送短信
def goip_send_sms():
    # 绑定浏览器
    Browser = webdriver.Chrome()
    # 打开页面
    url = "http://" + dev.ip + "/login_en.html"
    Browser.get(url)

    # 用户名的定位
    Browser.find_element_by_id("accountID").clear()
    Browser.find_element_by_id("accountID").send_keys(dev.username)
    time.sleep(0.5)
    # 密码的定位
    Browser.find_element_by_id("passwordID").clear()
    Browser.find_element_by_id("passwordID").send_keys(dev.password)
    time.sleep(0.5)
    # 点击登录
    Browser.find_element_by_id("btnLoginID").click()
    time.sleep(0.5)
    # 判断弹出内容，并处理
    result = expected_conditions.alert_is_present()(Browser)
    if result:
        result = Browser.switch_to.alert
        print(result.text)
        if "用户名或密码错误" in result.text:
            print("密码错误,停止测试")
            exit()
        else:
            result.accept()
    else:
        print("alert 未弹出")

    Browser.switch_to.frame(0)
    # 切换到左侧frame
    Browser.switch_to.frame("left")
    # 点击短信设置
    Browser.find_element_by_id("H4").click()
    # 点击短信发送
    Browser.find_element_by_xpath('//*[@id="M4"]/ul/li[2]/a/span').click()
    time.sleep(0.5)

    # 返回主页，重新选择frame
    Browser.switch_to.default_content()
    Browser.switch_to.frame(0)
    # 切换到右侧frame
    Browser.switch_to.frame("right")
    # 勾选第几个port
    SelectPort = "__ID_PortChkBoxes" + str(sim1.port)
    Browser.find_element_by_id(SelectPort).click()
    # 填写内容
    Browser.find_element_by_id("goip_sms_dst").click()
    Browser.find_element_by_id("goip_sms_dst").clear()
    Browser.find_element_by_id("goip_sms_dst").send_keys(sim2.phone)
    Browser.find_element_by_id("goip_sms_send").click()
    Browser.find_element_by_id("goip_sms_send").clear()
    Browser.find_element_by_id("goip_sms_send").send_keys("hello")

    # 点击发送
    Browser.find_element_by_id("ID_BtnSend").click()

    time.sleep(2)  # 点击完发送，先等一会儿等待消息更新
    # 关闭浏览器
    Browser.quit()

    check.test_step = 3   # 设置到下一个阶段，查询发送状态
    check.time_out = 0

    check.count += 1      # 发送一次短信加1，在goip_sms_stat_reptile里面要判断是否成功发送1条


# 查询卡注册状态
@try_fun
def goip_port_status():
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/port_status_en.html?username=" + dev.username + "&password=" + dev.password + "&period=0"
    requests_result = requests.get(requests_addr, timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        logging.info("code:%d" % requests_result.status_code)
        # logging.info(requests_result.text)

        port_status = re.findall("strPortStatus = '(.*?)'", requests_result.text)
        # logging.info(port_status)
        # findall返回的是list，取list的第一个元素转换成字典
        port_dict = json.loads(port_status[0])
        logging.info(port_dict)
        max_ports = port_dict["count"]
        logging.info("max_ports:%d" % max_ports)

        sim1_register = port_dict["data"][sim1.port - 1][4]   # 查看sim1注册状态
        sim1_slot = port_dict["data"][sim1.port - 1][2]       # 查看sim1当前在第几个卡槽
        sim2_register = port_dict["data"][sim2.port - 1][4]
        sim2_slot = port_dict["data"][sim2.port - 1][2]

        logging.info("sim1.slot:%s sim1.port:%s" % (sim1.slot, sim1.port))
        logging.info("sim2.slot:%s sim2.port:%s" % (sim2.slot, sim2.port))
        logging.info("sim1_slot:%s sim1_register:%s" % (sim1_slot, sim1_register))
        logging.info("sim2_slot:%s sim2_register:%s" % (sim2_slot, sim2_register))

        # 判断端口状态
        if (('Yes' == sim1_register) and (sim1.slot == sim1_slot)    # sim1，即发送短信的卡要在线且已经注册上
        and ('Yes' == sim2_register) and (sim2.slot != sim2_slot)):  # sim2，当前sim2不能在线
            logging.info("status ok")
            check.test_step = 2  # 设置到下一个阶段，发送短信
            check.time_out = 0
        else:
            check.time_out += 1
            logging.info("status ng,time_out:%s" % check.time_out)

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    return requests_result


def goip_clean_sms():
    # 绑定浏览器
    Browser = webdriver.Chrome()
    # 打开页面
    url = "http://" + dev.ip + "/login_en.html"
    Browser.get(url)

    # 用户名的定位
    Browser.find_element_by_id("accountID").clear()
    Browser.find_element_by_id("accountID").send_keys(dev.username)
    time.sleep(0.5)
    # 密码的定位
    Browser.find_element_by_id("passwordID").clear()
    Browser.find_element_by_id("passwordID").send_keys(dev.password)
    time.sleep(0.5)
    # 点击登录
    Browser.find_element_by_id("btnLoginID").click()
    time.sleep(0.5)
    # 判断弹出内容，并处理
    result = expected_conditions.alert_is_present()(Browser)
    if result:
        result = Browser.switch_to.alert
        print(result.text)
        if "用户名或密码错误" in result.text:
            print("密码错误,停止测试")
            exit()
        else:
            result.accept()
    else:
        print("alert 未弹出")

    Browser.switch_to.frame(0)
    # 切换到左侧frame
    Browser.switch_to.frame("left")
    # 点击短信设置
    Browser.find_element_by_id("H8").click()
    # 点击短信发送
    Browser.find_element_by_xpath('//*[@id="M8"]/ul/li[7]/a/span').click()
    time.sleep(0.5)

    # 返回主页，重新选择frame
    Browser.switch_to.default_content()
    Browser.switch_to.frame(0)
    # 切换到右侧frame
    Browser.switch_to.frame("right")

    # 清楚发送记录
    Browser.find_element_by_xpath('//*[@id="ID_SmsStatBox_Body"]/table[1]/tbody/tr/td[2]/div/input[3]').click()

    time.sleep(0.5)

    # 判断弹出内容，并处理
    result = expected_conditions.alert_is_present()(Browser)
    if result:
        result = Browser.switch_to.alert
        print(result.text)
        if (("确定要清除卡" in result.text)
         or ("Are you sure to clear the SIM" in result.text)):
            result.accept()
    else:
        print("alert 未弹出")

    time.sleep(2)  # 点击完发送，先等一会儿等待消息更新
    # 关闭浏览器
    Browser.quit()

    check.test_step = 1  # 设置到下一个阶段，查询卡注册状态
    check.time_out = 0


while True:

    if check.time_out >= 50:  # 超过50次都检测不成功，退出
        logging.info("time out stop")
        exit()

    if 0 == check.result:
        if 0 == check.test_step:    # 开始测试前，先清楚发生记录
            goip_clean_sms()
        elif 1 == check.test_step:  # 查询卡注册状态
            goip_port_status()
        elif 2 == check.test_step:  # 发送短信
            goip_send_sms()
        elif 3 == check.test_step:  # 查询发送状态
            goip_sms_stat_reptile()
        elif 4 == check.test_step:  # 切卡
            goip_switch_sim()
    else:
        logging.info("###### stop test ######")

    time.sleep(2)

