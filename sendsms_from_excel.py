#! /usr/bin/python3


import requests
import xlrd
import os
import time
import json
import logging
import pandas as pd
import random


def logging_init():
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)  # 设置logger日志等级

    # 创建handler
    output_file = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + "_add_mac"
    log_file = os.path.join(os.path.dirname(__file__) + output_file + ".log")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    ch = logging.StreamHandler()

    # 设置输出日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    )

    # 为handler指定输出格式，注意大小写
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 为logger添加的日志处理器
    logger.addHandler(fh)
    logger.addHandler(ch)

    return True

def read_num(excel_name):
    excel_fd = xlrd.open_workbook(excel_name)
    excel_sheet = excel_fd.sheet_by_index(0)
    num_list = excel_sheet.col_values(0)
    logging.info("num_list: %s", num_list[1:-1])
    str_list = list(map(int, num_list[1:-1]))
    logging.info('str_list is: ' + str(str_list))
    logging.info("num_total: %d", len(str_list))

    return str_list


def read_content(excel_name):
    excel_fd = xlrd.open_workbook()
    execl_sheet = excel_fd.sheet_by_index(0)
    content_list = execl_sheet.col_values(1)
    logging.info("content_list: %s", content_list[1:-1])
    logging.info("content_total: %d", len(content_list))

    return content_list[1:-1]


def http_requests():
    requests_url = "http://192.168.1.59/goip_post_sms.html?username=root&password=root"  # 这是请求地址
    data = {"type": "send-sms", "task_num": 1, "tasks": []}  # 这是data得默认值,tasks里面先是空，
    header_dict = {'Content-Type': 'application/json'}


if __name__ == '__main__':
    logging_init()

    num_list = read_num("100sms.xls")
    content_list = read_content("100sms.xls")

    requests_url = "http://192.168.1.59/goip_post_sms.html?username=root&password=root"  #这是请求地址
    data = {"type": "send-sms", "task_num": 1, "tasks":[]} #这是data得默认值,tasks里面先是空，
    header_dict = {'Content-Type': 'application/json'}

    # 将内容赋值到data中
    for i in range(1, 101):
        phone_num = num_list[i]
        sms_content = content_list[i]
        task = {"did": 1, "to": "111", "sms": "1"}
        task['did'] = i
        task['to'] = phone_num
        task['sms'] = sms_content
        data['tasks'].append(task)

    while True:

        #只post一次,需要在tasks[{},{}...]里面添加所有得，所以上面得for里面就是添加，post要tab回退一个
        logging.info("url: %s", requests_url)
        logging.info("data: %s", data)
        body = json.dumps(data)
        requests_result = requests.post(requests_url, data=json.dumps(data), data=body, headers=header_dict, timeout=(5, 5))
        logging.info(requests_result)
        requests_code = requests_result.status_code
        logging.info("code: %s", requests_code)

        # if requests_code = 200:
        #
        # else:
        #     exit()

        time.sleep(1)


        #
        # for i in range(0, 101):
        #     logging.info("i:%d",i)
        #     phone_num = num_list[i]
        #     # logging.info("first number is: %s", phone_num)拿现在我们就可以得到正确得data了，接下去request
        #     sms_content = content_list[i]
        #     # logging.info("first sms is: %s:", sms_content)
        #     data['tasks'][0]['did'] = i + 1
        #     data['tasks'][0]['to'] = phone_num
        #     data['tasks'][0]['sms'] = sms_content
        #     logging.info(data)
        #     body = json.dumps(data)
        #
        #     requests_result = requests.post(requests_url, data=body, headers=header_dict, timeout=(5, 5))
        #     requests_code = requests_result.status_code
        #     logging.info(requests_result)
        #     logging.info(requests_code)
        #
        #     time.sleep(5)



