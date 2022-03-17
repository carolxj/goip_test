#!/usr/bin/python3
'''
cars = ['audi', 'bmw', 'subarn', 'toyota']
# 示例
for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())

# 每条if语句的核心都是一个值为true或false的表达式，这种表达式成为条件测试，根据条件测试的值为true或false来决定
# 是否执行if语句种得代码，如果条件测试的值为true，就执行紧跟在if语句后面的代码；如果为false，就忽略这些代码.
# 检查是否相等,不考虑大小写lower（）函数可将变量值换成小别再将结果与原本变量比较（==）
# 检查是否不相等，（！=）
requested_tooping = 'mushrooms'
if requested_tooping != 'anchovies':
    print("\nhold the anchovies")

# 检查多个条件
age_0 = 18
age_1 = 25
if age_0 >= 21 and age_1 >= 21:
    print("ture")
else:
    print("false")
age_0 = 18
age_1 = 18
if age_0 >= 21 or age_1 >= 21:
    print("ture")
else:
    print("false")

# 检查特定值是否包含在列表中
requested_tooping = ['mushrooms', 'onions', 'pineapple']
if 'mushrooms' in requested_tooping:
    print("\nture")
else:
    print("false")

# 检查特定值是否不包含在列表中
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'
if user not in banned_users:
    print(user.title() + "," + "you can post a reponse if you wish.")
else:
    print("aaa")
'''
# 练习
num = 30
if num == 30:
    print("\nTure")

flower = 'Rose'
if flower.lower() == 'rose':
    print("\nture")

number_0 = 15
number_1 = 20
if number_0 == 15 and number_1 == 15:
    print("\nture")
else:
    print("\n false")
if number_0 >= 20 and number_1 >= 20:
    print("\nture")
else:
    print("false")

if number_0 <= 30 or number_1 <= 30:
    print("ture")
else:
    print("false")
colour = ['red', 'yellow', 'blue']
if 'red' in colour:
    print("I like red")
myfavorite_colour = 'purple'

if myfavorite_colour not in colour:
    print("I want add the purple")

# 5.3 if 语句

