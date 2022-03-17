#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support import expected_conditions

# 打开浏览器

option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
driver = webdriver.Chrome(options=option)

#访问网站
driver = webdriver.Chrome()
#打开网页
driver.get('http://www.testingedu.com.cn:8000/index.php')
