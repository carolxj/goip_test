#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: ye.lin
# Time: 2021/02/17
# Describe：


import requests
import logging
import os
import time
import json
import xlrd


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


def read_mac(excel_name):
    excel_fd = xlrd.open_workbook(excel_name)
    logging.info("sheet_names: %s", excel_fd.sheet_names())  # 获取所有sheet名字
    logging.info("sheets: %d", excel_fd.nsheets)  # 获取sheet数量
    excel_sheet = excel_fd.sheet_by_index(0)  # 第一个表
    mac_list = excel_sheet.col_values(3)   # 第二列数据
    logging.info("mac_list: %s", mac_list)
    logging.info("mac_len: %s", len(mac_list))

    return mac_list

if __name__ == '__main__':
    logging_init()

    gw_url = 'https://....'

    payload = {
        "devId": "649A08FC215D",
        "prodTypeId": "M02C02D02Z02",
        "data": [
            {
                "k": "firmwareModular",
                "v": "zgateway"
            },
            {
                "k": "version",
                "v": "2.1.9"
            },
            {
                "k": "md5",
                "v": "597afbddcd5920a73d3f4c320a61eb90"
            },
            {
                "k": "size",
                "v": "4158483"
            },
            {
                "k": "url",
                "v": "http://file.ziroom.com/g4m4/M00/06/79/ChAZYWFBtDyAf3TaAD90E8DNEh89054.gz"
            }
        ]
    }
    headers = {'content-type': 'application/json'}

    i = 1  # 第一行不为MAC地址
    gw_pass = 0

    mac_list = read_mac("OTA-1.xls")

    while i < len(mac_list):
        start_mac = mac_list[i]
        payload["devId"] = start_mac.upper()
        logging.info("gw_url: %s, payload: %s", gw_url, payload)
        try:
            result = requests.post(gw_url, data=json.dumps(payload), headers=headers, timeout=(25, 25))
            logging.info("result: %s", result.text)
            if result.status_code == 200:
                msg = json.loads(result.text)
                if (200 == msg["code"]) and ("success" == msg["message"]):
                    gw_pass += 1
                    logging.info("正式环境 i: %s, mac: %s, ota ok", i, start_mac)
                else:
                    logging.info("正式环境 i: %s, mac: %s, ota fail", i, start_mac)

            i += 1

        except Exception as e:
            logging.info("正式环境 i: %s, mac: %s, ota fail", i, start_mac)

        time.sleep(2)

    logging.info("正式环境添加成功%d台", gw_pass)

