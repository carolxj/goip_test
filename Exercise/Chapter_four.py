# for 循环
magicians = ['alice', 'david', 'carolina']
for magician in  magicians:
    print(magician)
magician_1 = magicians[:]
print(magician_1)

magicians =['alice', 'david', 'carolina']
for magician in  magicians:
    print(magician.title() + ", that was a great trick!" )
    print("I cat't wait to see your next trick," + magician.title() + ".\n")

print("Thank you, everyone. That was a great magic show1")

#练习
pizzas = ['\ndurian pizza', 'superme pizza', 'ham pizza']
for pizza in pizzas:
    print(pizza)
    print(pizza + ", I like pepperoni pizza\n")
print("I really love pizza")

animals = ['\nrabbit', 'chicken', 'dog']
for animal in animals:
 #   print(animal)
    print(animal.title() + ", would make a great pet!")
print("Any of there animals would name a great pet!\n")

# 创建数值列表
for value in  range(1,2): # 使用函数
    print(value)
 # 使用range()创建数字列表
numbers = list(range(1,6))
print(numbers)

even_numbers = list(range(2,21,2)) # 打印21以内的偶数，这里表示从2开始数，不断加2
print(even_numbers)

squares = []
for value in range(1,11):
    square = value**2 # 列表元素乘方，**表示
    squares.append(square)
print(squares)

#列表解析
squares = [value**2 for value in range(1,21)]
print(squares)

#练习
for value in range(1,21):
    print(value)

#numbers = list(range(1,1000000))
#for number in numbers:
#    print(number)

numbers = list(range(1,1000001))
print(max(numbers)) # 最大值
print(min(numbers)) # 最小值
print(sum(numbers)) # 求和
# 奇数
odd_numbers = list(range(1,21,2))
for odd_number in odd_numbers:
    print(odd_number)
# 倍数

#立方
cube_numbers = [value**3 for value in range(1,10)]
print(cube_numbers)

cube_numbers =[]
for value in range(1,10):
    cube_number = value**3
    cube_numbers.append(cube_number)
print(cube_numbers)

#切片
players = ['chatles', 'martina', 'michael','florence','eli']
print(players[1:2]) # :前是开始元素索引，：后是借宿元素索引
print(players[-2:]) # 倒数最后两个元素
#遍历切片
players = ['charled', 'martina','michael','florence', 'eli']
print("Here are the first three players on my team:")
for player in players[:3]:
    print(player.title())

#复制列表
my_foods =['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]
print("\nMy favorite foods are：")
print(my_foods)

print("\nMy friend's favorite foods are:")
print(friend_foods)

my_foods.append('cannoli')
friend_foods.append('ice cream')

print("\nMy favorite foods are:")
print(my_foods)

print("\n My friend's favorite foods are:")
print(friend_foods)

#练习

#元组
foods = ('beef', 'chicken', 'cake', 'pizza', 'egg')
for food in  foods:
    print(food)