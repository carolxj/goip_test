#!/usr/bin/python

import requests
import os
import logging
import time
import functools


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
dev = DevInfo("192.168.1.58", "80", "root", "root123")
# dev = DevInfo("192.168.1.60", "80", "root", "root")
# dev = DevInfo("192.168.1.54", "80", "root", "root")


class SwitchInfo(object):
    def __init__(self, result, count, start_time, use_time):
        self.result = result  # 判断模块是否检测完成，0-未完成，1-完成
        self.count = count  # 测试次数
        self.start_time = start_time  # 测试起始时间
        self.use_time = use_time  # 测试用时


    time_out = 0
    old_iccid = {}
    new_iccid = {}
    old_imsi = {}
    new_imsi = {}


switch = SwitchInfo(0, 0, time.time(), 0)
switch.old_iccid = {'01': "first", '02': "first", '03': "first", '04': "first"}
switch.old_imsi = {'01': "first", '02': "first", '03': "first", '04': "first"}
switch.new_iccid = {'01': "first", '02': "first", '03': "first", '04': "first"}
switch.new_imsi = {'01': "first", '02': "first", '03': "first", '04': "first"}


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
def modem_check_fun():

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


# 当服务器连不上，request会报错，所以需要加一个重试机制
'''
@try_fun
def dev_reboot_fun():

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
'''

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
        logging

    switch.start_time = time.time()

    return requests_result


# 获取当前卡所在位置
# modemid: 1-max_ports
@try_fun
def get_sim_fun(modemid):

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

        if (modemid > max_ports) or (modemid <= 0):
            logging.info("modemid:%d" % modemid)
            return "error"

        # 获取现在模块使用那个port的卡
        sim_slot = result_dict["status"][modemid - 1]["port"]
        sim_slot = sim_slot[2:4]  # 这边以前是获取A/B/C/D,现在要获取后面的01,02
        logging.info("sim_slot:%s" %sim_slot)
        # 判断同一个port获取到的iccid/imsi是否与上一次一致
        switch.new_iccid[sim_slot] = result_dict["status"][modemid - 1]["iccid"]
        switch.new_imsi[sim_slot] = result_dict["status"][modemid - 1]["imsi"]
 #       switch.new_imei[sim_slot] = result_dict["status"][modemid - 1]["imei"]
        sim_status = result_dict["status"][modemid - 1]["st"]
        logging.info("sim_slot: %s, newiccid:%s, newimsi:%s" % (sim_slot, switch.new_iccid[sim_slot], switch.new_imsi[sim_slot]))
        logging.info("sim_slot: %s, oldiccid:%s, oldimsi:%s" % (sim_slot, switch.old_iccid[sim_slot], switch.old_imsi[sim_slot]))

        logging.info("sim_status: %d" % sim_status)

        # 判断是否切卡成功
        if (3 == sim_status) or (4 == sim_status):
            switch.time_out = 0
            switch.use_time = time.time() - switch.start_time
            logging.info("Switch Count: %d ,use time:%s" % (switch.count, switch.use_time))
            switch.count += 1

            if switch.old_iccid[sim_slot] == "first":  # 第一次赋值
                switch.old_iccid[sim_slot] = switch.new_iccid[sim_slot]
                switch.old_imsi[sim_slot] = switch.new_imsi[sim_slot]
 #               switch.old_imei[sim_slot] = switch.new_imei[sim_slot]

            else:
                if switch.new_iccid[sim_slot] == switch.old_iccid[sim_slot]:
                    if sim_slot == "01":
                        switch_sim_fun(modemid, "02")
                    elif sim_slot == "02":
                        switch_sim_fun(modemid, "03")
                    elif sim_slot == "03":
                        switch_sim_fun(modemid, "04")
                    else:
                        switch_sim_fun(modemid, "01")
                else:
                    switch.result = 1
                    logging.info("switch iccid error exit!")
        else:
            logging.info("switch_result ng count: %d" % switch.time_out)
            switch.result = 0
            switch.time_out += 1

    else:
        assert requests_code == 200  # 状态码不是200，也会报错并充实
        logging.info("code:%d" % requests_code)

    def recovery_fun():
     # 绑定浏览器
     Browser = webdriver.Chrome()
     # 最大化浏览器
     Browser.maximize_window()
     # 打开页面
     url = "http://" + dev.ip + "/login_en.html"
     Browser.get(url)
     # 用户名的定位
     Browser.find_element_by_id("accountID").clear()
     Browser.find_element_by_id("accountID").send_keys(dev.username)
     time.sleep(1)
     # 密码的定位
     Browser.find_element_by_id("passwordID").clear()
     Browser.find_element_by_id("passwordID").send_keys(dev.password)
     time.sleep(1)
     # 点击登录
     Browser.find_element_by_id("btnLoginID").click()
     time.sleep(1)
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
     #点击系统设置
     Browser.find_element_by_id('H7').check()
     #点击文件管理(//*[@id="M7"]/ul/li[5]/a/span）
     Browser.find_element_by_xpath('//*[@id="M7"]/ul/li[5]/a/span').check()
     #点击日志导出(//*[@id="ID_TabFileList"]/tbody/tr[1]/td[7]/input[2])
     Browser.find_element_by_xpath('//*[@id="ID_TabFileList"]/tbody/tr[1]/td[7]/input[2]').check()
     # 返回主页，重新选择frame(不知道为什么要这样做)
     Browser.switch_to.default_content()
     Browser.switch_to.frame(0)

  


    return requests_result


while True:

    if check.time_out >= 50:   # 超过30次都检测不到模块，退出
        exit()
    if switch.time_out >= 50:  # 超过30次还没切卡完成，退出
        exit()

    if 0 == check.result:
        modem_check_fun()
    else:
        if 0 == switch.result:

            get_sim_fun(1)
        else:
            exit()
    time.sleep(2)

