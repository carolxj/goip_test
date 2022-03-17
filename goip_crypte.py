#! /usr/bin/python3

import hashlib
import requests
import json
import os
import logging
import time
from Crypto.Cipher import ARC4, AES

class CheckInfo(object):
    def __init__(self, result, start_time, use_time):
        self.result = result  #结果
        self.start_time = start_time #测试起始时间
        self.use_time = use_time # 测试用时

        time_out = 0

'''class DevInfo(object):
    def __init__(self, ip, username, password, expires, cnonce):
        self.ip = ip  # 设备IP
        self.username = username  # 用户名
        self.password = password  # 密码
        self.expires = expires  # 超时时间
        self.cnonce = cnonce  # 随机码

dev = DevInfo("192.168.1.59", "root", "root", "60", "123456")'''
check = CheckInfo(0, time.time(), 0)
check.time_out = 0
username = "root"
password = "root"
cnonce = "123456"
expires = "60"
ip = "192.168.1.57"
url_resource = "/crypt_sess.json"
url_request = ip + url_resource

def calc_client_session(username, password, cnonce, url_resource):
        m = hashlib.md5()
        m.update(username.encode())
        m.update(password.encode())
        m.update(cnonce.encode())
        m.update(url_resource.encode())
        logging.info(m.hexdigest())
        return m.hexdigest()

def calc_req_auth(username, password, server_session, url_resource, req):
        m = hashlib.md5()
        m.update(username.encode())
        m.update(password.encode())
        m.update(server_session.encode())
        m.update(url_resource.encode())
        m.update(str(req).encode())
        logging.info(m.hexdigest())
        return m.hexdigest()

def calc_key(username, password, client_session, server_session, req):
        m = hashlib.md5()
        m.update(username.encode())
        m.update(password.encode())
        m.update(client_session.encode())
        m.update(server_session.encode())
        m.update(str(seq).encode())
        logging.info(m.hexdigest())
        return m.hexdigest()

def arc4_enc(key, data):
        cipher = ARC4.new(key.encode())
        return cipher.decrypt(data.encode())

def aes_ecb_enc(key, data):
        bs = AES.block_size
        pad = lambda s: s + b"\0" * (bs - len(s) % bs)
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        return cipher.encrypt(pad(data.encode()))




if False == os.path.exists("log"):
    print("log file don't exist.create.")
    os.major("log")
else:
    print("log file exist")

logging.basicConfig(  # filename="log/goip_crypte.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



logging.info("###########################test start##################################")


client_session = calc_client_session(username, password, cnonce, url_resource)
crypt_params = {
        'username': username,
        'password': password,
        'cnonce': cnonce,
        'url_resource': url_resource
        }

req = requests.get(url_request, params=crypt_params)
response = req.json()
logging.info(response)

