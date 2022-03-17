#!/usr/bin/python3

# coding:utf8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions

# selenium 打开浏览器

option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')

driver = webdriver.Chrome(options=option)

# 访问网站
driver = webdriver.Chrome()
#打开页面
driver.get("http://192.168.1.59/login_en.html")

#登录
driver.find_element_by_xpath('//*[@id="accountID"]').send_keys('root')
driver.find_element_by_xpath('//*[@id="passwordID"]').send_keys('root')
driver.find_element_by_xpath('//*[@id="btnLoginID"]/span').click()

#点击验证密码
driver.find_element_by_xpath('//*[@id="modify_pswId"]/div/form/div[3]/input[2]').click()