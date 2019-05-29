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


GOIP_OK = 1
GOIP_FAIL = 0

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


class Httpmsg():
    headers = ""
    cookies = ""


check = CheckInfo(0, 0, time.time(), 0)
check.time_out = 0
dev = DevInfo("43.249.29.213", "55962", "root", "root123")
httpmsg = Httpmsg()

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


def md5value(s):
    password = hashlib.md5()
    password.update(s.encode(encoding='utf-8'))
    print('password:', password.hexdigest())
    return password.hexdigest()


def send_AT_command():
    # 绑定浏览器
    Browser = webdriver.Chrome()
    # 最大化浏览器
    Browser.maximize_window()
    # 打开页面
    url = "http://" + dev.ip + ":" +dev.port + "/login_en.html"
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
    return GOIP_OK

def check_AT_result():
    # 发送get请求获取goip_command页面
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/goip_command_en.html"
    response = requests.get(requests_addr, headers=httpmsg.headers)
    print(response.text)

    if 200 == response.status_code:
        print("check ok")
        ATCmdResp = re.findall("strCmdResp = '(.*?)'", response.text)
        print(ATCmdResp)
        AT_dict = json.loads(ATCmdResp[1])
        print(AT_dict)
        max_ports = AT_dict["count"]
        print(max_ports)
        i = 0
        for i in range(max_ports):
            ATCmdResp[i] = AT_dict["data"][i][4]
            print(ATCmdResp[i])



def login():
    url = "http://" + dev.ip + ":" + dev.port + "/login_en.html"
    httpmsg.headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.get(url, headers=httpmsg.headers)
    # print(response.text)
    cookies_nonce = re.findall('var cookies_nonce = "(.*?)";', response.text)
    print(cookies_nonce[0])

    s = "root:" + "root123:" + cookies_nonce[0]
    passwordmd5 = md5value(s)

    encoded_value = "root:" + passwordmd5
    params = {"nonce": "",
             "encoded" : encoded_value,
            "loginStatus" : "",
         }

    # http请求头
    httpmsg.cookies = "username=5;" "auth_00a277=" + cookies_nonce[0]
    httpmsg.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "cookie": httpmsg.cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    response = requests.post(url, headers=httpmsg.headers, data=params)
    # print(response.text)
    loginStatus = re.findall('id="ID_LoginStatus" name="loginStatus" value="(.*?)"',response.text)
    print(loginStatus[0])

    if loginStatus[0] == '0':
        return GOIP_OK
    else:
        GOIP_FAIL


def port_status():
    # 发送get请求获取post_status页面
    print(httpmsg.headers)
    requests_addr = "http://" + dev.ip + ":" + dev.port + "/port_status_en.html"
    response = requests.get(requests_addr, headers=httpmsg.headers)
    # print(response.text)
    requests_code = response.status_code

    if 200 == requests_code:
        print("code:%d" % response.status_code)
        # print(response.text)

        port_status = re.findall("strPortStatus = '(.*?)'", response.text)
        print(port_status)
        # findall返回的是list，取list的第一个元素转换成字典
        port_dict = json.loads(port_status[0])
        print(port_dict)
        max_ports = port_dict["count"]
        print(max_ports)

        # 读取at命令返回的内容，并判断响应是否正常
        modem_status = {}
        check_ng = 0
        i = 0
        for i in range(max_ports):
            modem_status[i] = port_dict["data"][i][3]
#            print( modem_status[i])
            # 判断模块是否都返回，只要有一个不正常则置标志位
            if ("Yes" != modem_status[i]):
                check_ng = 1
#                logging.info("modem %d ng,result:%s" % (i + 1, modem_status[i]))

        if 0 == check_ng:
             print("module check ok")
             return GOIP_OK
        else:
            print("check_result ng count: %d" % check.time_out)
            return GOIP_FAIL
    else:
         return GOIP_FAIL

if login() == GOIP_OK:
    print("login success")
else:
    print("login failed")
    exit()

while True:

    if port_status() == GOIP_OK:
        print("login success")

        if send_AT_command() == GOIP_OK:
            check_AT_result()

    else:
        exit()

    time.sleep(2)


