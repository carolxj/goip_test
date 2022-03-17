#! /user/bin/python3

# 遍历切片
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print("Here atr the first three players on my team:")
for player in players[:3]:
    print(player.title())

# 复制列表
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]

print("my favorite foods are:")
print(my_foods)
print("\nmy friend's favorite foods are:")
print(friend_foods)

my_foods.append('cannoli')
friend_foods.append('ice cream')

print("my favorite foods are:")
print(my_foods)

print("my friend's faoverite foods are:")
print(friend_foods)

# exercise
# 使用切片打印列表的前三个元素
my_foods = ['cake', 'hamburger', 'chicken', 'beef']
print("The first three items in the list are:")
for my_food in my_foods[:3]:
    print(my_food.title())
# 在列表中增加一个元素并打印
print("\nThere items from the middle of the list are:")
my_foods.append('ice cream')
print(my_foods)

# 使用切片打印列表中间的三个元素
print("\nThere items from the middle of the list are:")
print(my_foods[1:4])

# 使用切片打印列表末尾的三个元素
print("\nThe last three items in the list are:")
print(my_foods[-3:])

# 复制列表
my_pizzas = ['Durian pizza', 'Ham pizza', 'Fruit pizza']
friend_pizzas = my_pizzas[:]
my_pizzas.append('mushroom pizza')
friend_pizzas.append('cheese pizza')
print("my favorite pizzas are:")
for my_pizza in my_pizzas:
    print(my_pizza.title())
print("\nmy friend's favorite pizzas are:")
for friend_pizza in friend_pizzas:
    print(friend_pizza.title())

# 4.5 元组（圆括号而不是方括号）
dimensions = (200, 100)
print(dimensions[0])
print(dimensions[1])

# 遍历元素表中的所有值
dimensions = (200, 50)
for dimension in dimensions:
    print(dimension)
# 修改元素
dimensions = (200, 50)
print("original dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 200)
print("\nmodified dimensions:")
for dimension in dimensions:
    print(dimension)

# 练习
foods = ('cake', 'chicken', 'hambuger', 'beef', 'noodles')
for food in foods:
    print(food)
foods = ('egg tart', 'bread', 'humbuger', 'beef', 'noodles')
print("\nThis is new menu:")
for food in foods:
    print(food)

