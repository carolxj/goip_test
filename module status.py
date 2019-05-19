#!/usr/bin/python

class CheckInfo(object)
    def __init__(self, result, count, start_time, use_time ):
        self.result = result #判断模块是否检测完成，0-未完成 ，1-完成
        self.count = count #测试次数
        self.start_time = start_time #测试起始时间
        self.use_time =use_time #测试用时


    time_out =0

class DevInfo(object)
    def __init__(self, ip, port, username, password):
        self.ip = ip #设备ip地址
        self.port =port #访问设备默认端口80
        self.username = username #登录设备用户名
        self.password = password #登录设备密码


check = CheckInfo(0,0,time.time(),0)
check.time_out = 0
dev = DevInfo("192.168.1.59","80","root","root123")


