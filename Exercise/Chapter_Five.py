# if 语句
'''cars = ['addi', 'bmw', 'subaru', 'toyota']
for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())

# 条件测试( Python根据条件测试的值为True 还是False 来决定是否执行if 语句中的代码。如果 条件测试的值为True ，Python就执行紧跟在if 语句后面的代码；如果为False ，Python就忽略这些代码。
requested_topping = 'mushrooms'
if requested_topping != 'anchovies':
    print("\nhold the anchovies!")

answer = 18
if answer != 20:
    print("\nthat is mot the correct answer,please try again!")
# 使用and检查多个条件
age_1 = 18
age_2 = 20
if age_1 >= 21 and age_2 >= 21:
    print("\nture")
else:
    print("flase")
# 使用or检查多个元素
age_1 = 20
age_2 = 22
if age_2 >= 10 or age_1 <= 25:
    print("\nY")
else:
    print("\nN")
# 使用in检查特定值是否包含在列表中
requested_topping = ['mushrooms', 'onions', 'pineapple']
if 'mushroms' in requested_topping:
    print("Ture")
else:
    print("False")
# 检查特定值是否不包含在列表中
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'

if user not in banned_users:
    print(user.title() + ", \nyou can post a response if you wish.")

# 简单的if语句
age = 19
if age >= 18:
    print("You are old enough to vote")

if age >= 20:
    print("have you registered to vote yet?")
else:
    print("sorry,you are too young to vote")
    print("please register to vote as soon as you turn 19!")

# if-elif-else结构
# 4岁以下免费
# 4-18岁收费5美元
# 18岁和18岁以上收费10美元
age = 12
if age < 4:
    print("\nyour admission cost is $0.")
elif age < 18:
    print("\nyour admission cost is $5.")
else:
    print("\nyour admission cost is $10.")
# 省略else代码
age = 40
if age < 4:
    price = 0
elif age < 18:
    price =5
elif age < 65:
    price = 10
elif age >= 65:
    price = 5
print("your admission cost is $" + str(price) + ".")

# 测试多个条件
requested_topping = ['mushrooms', 'extra cheese']
if 'mushrooms' in requested_topping:
    print("\nAdding mushrooms")
if 'pepperoni' in requested_topping:
    print("Adding pepperoni")
if 'extra cheese' in requested_topping:
    print('Adding extra cheese')
print("\nFinished making your pizza!")

# 练习5-3#1
alien_color = ['green', 'yellow', 'red']
if 'green' in alien_color:
    print('You get 5 points')

alien_color = ['green', 'yellow', 'red']
if 'blue' in alien_color:
    print("You get 10 points")

# 2
alien_color = ['green', 'yellow', 'red']
if 'yellow' in alien_color:
    print("You get 5 points")

alien_color = ['green', 'yellow', 'red']
if 'bule' in alien_color:
    print("you get 5 points")
else:
    print("\nYou get 10 points")

# 3
alien_color = ['green', 'yellow', 'red']
if 'green' in alien_color:
    print("\nYou get 5 points")
elif 'yellow' in alien_color:
    print("you get 10 points")
else:
    print("error")
alien_color = ['green', 'yellow', 'red']
if'yellow' in alien_color:
    print("You get 10 points")
elif 'red' in alien_color:
    print("You get 15 points")
else:
    print("you not get any points")
alien_color = ['green', 'yellow', 'red']
if 'red' in alien_color:
    print("You get 15 points")
elif 'yellow' in alien_color:
    print("you not get 10 points")
else:
    print("error")

# 5-6
age = 70
if age < 2:
    print("He is a baby")
elif age < 4:
    print("He began to learn to walk")
elif age < 13:
    print("He is a children")
elif age < 20:
    print("He is adolescent")
elif age < 65:
    print("He is adult")
else:
    print("he is old people")

# 5-7
favorite_fruits = ['grape', 'watermelon', 'orange']
if "grape" in favorite_fruits:
    print("grape")
if "watermelon" in favorite_fruits:
    print("watermelon")
if "orange" in favorite_fruits:
    print("orange")
if "banana" in favorite_fruits:
    print("bananas")
if "buleberry" in favorite_fruits:
    print("buleberry")

# 检查特殊元素
requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
for requested_topping in  requested_toppings:
    print("Adding" + requested_topping + ".")
print("\nFinished making your pizza!")

requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']
for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print("\nsorry,we are out of green peppers right now.")
    else:
        print("Adding " + requested_topping + '.')

requested_toppings = []
if requested_toppings:
    for requested_topping in requested_toppings:
        print("Adding " + "requested_topping" + ".")
    print("\nFinished making your pizza!")
else:
    print("\nAre you sure you want a plain pizza?")

available_topping = ['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese']
requested_toppings = ['mushrooms', 'french fries', 'extra cheese']

for requested_topping in requested_toppings:
    if requested_topping in available_topping:
        print("Adding " + requested_topping + ".")
    else:
        print("Sorry,we don't have " + requested_topping + ".")
print("\nFinished making your pizza!")
'''
# 练习5-8
names = ['user', 'admin', 'operator', 'sales', 'officer']
if 'admin' in names:
    print('htllo admin,would you like to see a status report?\n')
else:
    print('hello eric,think you for logging in again.\n')

# 5-9
if not names:
    print("We need to find some users!")
else:
        del names[0:5]
        print(names)

# 5-10
current_users = ['Sunny', 'Mary','Linda', 'Elizabeth', 'Susan']
new_users = ['Mary', 'Susan', 'Jennifer', 'Sherry', 'Laura']
for new_user in new_users:
    if new_user in current_users:
        print("The user " + new_user + " is used,please change another user!\n")
    else:
        print(new_user + " is not be used!")

# 5-11
numbers = list(range(1,10))
print(numbers)
