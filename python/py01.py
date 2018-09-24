message = "One of Python's"
print(message)
print(3 ** 2)
# 创建列表
name = ['ricardo', 'bob', 'lucc']
print(name)
# 向列表末尾添加数据
name.append('walter')
print(name)
# 向列表0位置增加数据
name.insert(0, 'nazz')
print(name)
# 删除一条数据
del name[0]
print(name)
# 删除末尾数据
name.pop()
print(name)

# 按值删除
name.remove('bob')
# 临时排序 sorted
print(sorted(name))

# 临时排序反序
print(sorted(name, reverse = True))

# 确定列表长度
print(len(name))

# 列表反转
name.reverse()
print(name)

# 永久性排序 sort
name.sort()
# print(name)

# 永久性排序 倒叙  不能直接写在print里面
name.sort(reverse = True)
print(name)

for n in name:
	print(n)

# 使用range函数
for value in range(1, 5):
	print(value)

for value in range(1, 10, 2):
	print(value)

num_list = list(range(1, 5, 2))
print(num_list)

print(max(num_list))
min(num_list)
sum(num_list)

# 定义元祖
name_tuple = ('bob', 'walter')
print(name_tuple)
# name_tuple[0] = 'nazz'  错误
name_tuple = ('lucc')
print(name_tuple)



































