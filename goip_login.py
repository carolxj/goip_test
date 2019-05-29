#!/usr/bin/python

import requests
import functools
import time
import os
import logging
import re
import hashlib
import json
import sys
import io
import urllib.request
import http.cookiejar
from selenium import webdriver
from selenium.webdriver.support import expected_conditions



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
dev = DevInfo("192.168.1.58", "80", "root", "root123")

'''
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
'''

url = "http://" + dev.ip + "/login_en.html"
body = {}
headers = {'content-type':"application/x-www-form-urlencoded"}
response = requests.post(url, headers = headers)
# print(response.text)
cookies_nonce = re.findall('var cookies_nonce = "(.*?)";', response.text)
print(cookies_nonce[0])


def md5value(s):
    password = hashlib.md5()
    password.update(s.encode(encoding='utf-8'))
    print('password:', password.hexdigest())
    return password.hexdigest()

s = "root:" + "root123:" + cookies_nonce[0]
passwordmd5 = md5value(s)


url = "http://" + dev.ip + "/login_en.html"
encoded_value = "root:" + passwordmd5
params = {"nonce":"",
         "encoded" : encoded_value,
        "loginStatus" : "",

     }
# http请求头
cookies = "username=5;" "auth_00bf41=" + cookies_nonce[0]
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "cookie": cookies,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
response = requests.post(url, headers = header, data=params)
# print(response.text)
loginStatus = re.findall('id="ID_LoginStatus" name="loginStatus" value="(.*?)"',response.text)
print(loginStatus[0])


# 发送get请求获取post_status页面
requests_addr = "http://" + dev.ip + "/port_status_en.html"
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "cookie": cookies,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
response = requests.get(requests_addr, headers = header)
# print(response.text)



def goip_command_reptile():
    requests_addr = "http://" + dev.ip + "/port_status_en.html"
    requests_result = requests.get(requests_addr, headers = header,timeout=(5, 5))
    requests_code = requests_result.status_code

    if 200 == requests_code:

        print("code:%d" % requests_result.status_code)
        #print(requests_result.text)

        port_status = re.findall("strPortStatus = '(.*?)'", requests_result.text)
        #print(port_status)
        # findall返回的是list，取list的第一个元素转换成字典
        port_dict = json.loads(port_status[0])
        print(port_dict)
        max_ports = port_dict["count"]
        print(max_ports)

        # 读取at命令返回的内容，并判断响应是否正常
        modem_status = {}
        check_ng = 0
        for i in range(max_ports):
            modem_status[i] = port_dict["data"][i][3]
#            print(modem_status[i])
            # 判断模块是否都返回，只要有一个不正常则置标志位
            if (("" != modem_status[i])
            and ("ati\\r\\nQuectel\\r\\nEC25\\r\\nRevision: EC25AFAR05A04M4G\\r\\nOK" != modem_status[i])
            and ("AT No Response" != modem_status[i])):
                check_ng = 1
#                logging.info("modem %d ng,result:%s" % (i + 1, modem_status[i]))

        if 0 == check_ng:
             print(modem_status)

             check.use_time = time.time() - check.start_time
             print("test: %d ,use time:%s" % (check.count, check.use_time))
             check.count += 1

             check.start_time = time.time()

             check.result = 0
             check.time_out = 0  # 超时清零

        else:
            print("check_result ng count: %d" % check.time_out)
            check.result = 1
            check.time_out += 1  # 超时加1

            print(modem_status)

            check.use_time = time.time() - check.start_time
            logging.info("test: %d ,use time:%s" % (check.count, check.use_time))
            check.count += 1

            check.start_time = time.time()

    else:
         assert requests_code == 200  # 状态码不是200，也会报错并充实
         logging.info("code:%d" % requests_code)

    return requests_result


def send_AT_command():
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
    time.sleep(0.5)
    # 密码的定位
    Browser.find_element_by_id("passwordID").clear()
    Browser.find_element_by_id("passwordID").send_keys(dev.password)
    time.sleep(0.5)
    # 点击登录
    Browser.find_element_by_id("btnLoginID").click()
    time.sleep(0.5)
    #点击取消重置密码
    # 判断弹出内容，并处理
    result = expected_conditions.alert_is_present()(Browser)
    if result:
        result = Browser.switch_to.alert
        print(result.text)
        if "用户名或密码错误" in result.text:
            #点击取消
           # Browser.find_element_by_xpath("//*[@id="modify_pswId"]/div/form/div[3]/input[2]").check()
            print("密码错误,停止测试")
            exit()
        else:
            result.accept()
    else:
        print("alert 未弹出")
    Browser.switch_to.frame(0)
    # 切换到左侧frame
    Browser.switch_to.frame("left")
    # 点击网关设置
    Browser.find_element_by_id("H3").click()
    time.sleep(0.5)
    # 点击AT命令
    Browser.find_element_by_xpath('//*[@id="M3"]/ul/li[9]/a/span').click()
    time.sleep(0.5)

    # 返回主页，重新选择frame
    Browser.switch_to.default_content()
    Browser.switch_to.frame(0)
    # 切换到右侧frame
    Browser.switch_to.frame("right")
    # 勾选所有
    Browser.find_element_by_id("__ID_PortChkBoxesAll").click()
    time.sleep(0.5)
    # AT命令定位
    Browser.find_element_by_id("ID_goip_at_cmd").clear()
    Browser.find_element_by_id("ID_goip_at_cmd").send_keys("ati")
    time.sleep(0.5)
    # 执行命令
    Browser.find_element_by_xpath('//*[@id="ID_UssdCommandBox_Body"]/table[2]/tbody/tr[2]/td[2]/input[2]').click()
    time.sleep(1)
    time.sleep(1)    # 点击完AT发送，先等一会儿等待消息更新
    # 关闭浏览器
    Browser.quit()

    logging.info("send_AT_command ok")
    check.result = 1


while True:

    if  check.time_out >= 20:  # 超过20次都没有回复，退出
        logging.info("time out stop")
        exit()

    if 0 == check.result:
       send_AT_command()
    else:
        goip_command_reptile()

    time.sleep(2)


