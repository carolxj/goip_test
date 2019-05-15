#coding=utf-8
from selenium import webdriver
import unittest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class TestLogin(unittest.TestCase)
#指定设备登录
   def setUp(self):
       self.driver = webdriver.Firefox()
       #打开url
       self.driver.get("http://192.168.1.159/login")

       #登录操作
       def test_login(self)
           title = self.driver.title
           print title
           now_url = self.driver.current_url
           print now_url
           username = "root"
           password = "123456"
           #执行登录操作
           #用户名的定位
           self.driver.find_element_by_id("uaername").clear()
           self.driver.find_element_by_id("username").send_keys(username)
           #密码的定位
           self.driver.find_element_by_id("password").clear()
           self.driver.find_element_by_id("password").send_keys(password)
           #点击登录
           self.driver.find_element_by_css_selector(".btn.btn-success.btn-block").click()
           #登录成功
           login_name =
        self.driver.find_element_by_xpath('html/body/div[2]/ul/li[1]/a/strong').text
           login_name = login_name.strip()
       assert  login_name == uaername
#关闭

    self.driver.quit()


if _name_ == "_main_":
    unittest.main()