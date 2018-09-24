# 关键字实参
# def describe_pet(animal_type, pet_name):
# 	print('\n I have a ' + animal_type + '.')
# 	print('my' + animal_type + "'s name is " + pet_name.title())

# describe_pet(animal_type='hamster', pet_name='harry')

# 默认值实参  默认参数必须放在后面
# def describe_pet(pet_name, animal_type='dog'):
# 	print('\n I have a ' + animal_type + '.')
# 	print('my' + animal_type + "'s name is " + pet_name.title())

# describe_pet(pet_name='harry')

# 由于传递列表实参，在函数中修改列表会将整个原列表修改，所以用切片方式传递列表副本，保留原列表

# def function(list_name[:]):
# 	pass

# 传递任意数量实参, 传进来是一个元祖

# def make_pizza(*top):
# 	print(top)


# make_pizza('pep')

# make_pizza('hello', 'pizza', 'hello')

# 结合位置实参和任意数量实参, 按位置取的

# def make_pizza(name, *top):
# 	print(name)
# 	print(top[0].title())


# make_pizza(12, 'pep')

# make_pizza('hello', 'pizza', 'hello')

# 使用任意数量的关键字实参。字典形式dict

def build_profile(first, last, **user_info):
	profile = {}
	profile['first_name'] = first
	profile['last_name'] = last
	for key, value in user_info.items():
		profile[key] = value

	return profile

user_info = build_profile('walter', 'ricardo', location='princeton', field='physics')

print(user_info)








