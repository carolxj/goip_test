# 字典
alien_0 = {'color': 'green', 'points': '5'}
print(alien_0['color'])
print(alien_0['points'])

new_points = alien_0['points'] # 从字段alien_0中获取与points相关联的值并存储在变量new_points中
print("You just earned " + str(new_points) + " points!\n")

alien_0['x_position'] = 0 # 增加键_值对
alien_0['y_position'] = 25
print(alien_0)

alien_0 = {} # 给空字典添加键——值
alien_0['color'] = 'green'
alien_0['points'] = 10
print(alien_0)

alien_0 = {'color': 'green'}
print("\nThe alien is " + alien_0['color'] + '.')
alien_0['color'] = 'yellow'
print("The alien is now " + alien_0['color'] + ".")

alien_0 = {'x_position': '0', 'y_position': '25', 'speed': 'medium'}
print("\nOriginal x-position: " + str(alien_0['x_position']))

# 向右移动外星人
# 根据外星人当前速度决定将其移动多远
if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
    # 这个外星人的速度一定很快
    x_increment = 3
# 新位置等于老位置加上增量
alien_0['x_position'] = alien_0['x_position'] + str(x_increment)
print("New x_position: " + alien_0['x_position'])


# 删除
alien_0 = {'color': 'green', 'points': 5}
del alien_0['points']
print(alien_0)

# 由类似对象组成的字典
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python‘'
    }
print("\nSarah's favorite language is " + favorite_languages['sarah'].title() + '.')
