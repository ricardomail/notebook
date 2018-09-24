class Dog():
	"""模拟小狗的简单类"""
	def __init__(self, name, age):
		"""初始化小狗"""
		self.name = name
		self.age = age

	def sit(self):
		"""模拟小狗蹲下的命令"""
		print(self.name.title() + " is now sitting")

	def roll_over(self):
		"""模拟小狗打滚"""
		print(self.name.title() + " rolled over")

# my_dog = Dog('wally', 3)
# print(my_dog.name.title())
# print(my_dog.age)
# my_dog.sit()
# my_dog.roll_over()

# 可以直接修改属性值，  
class Car():
	"""一次模拟汽车的简单尝试"""
	def __init__(self, make, model, year):
		self.make = make
		self.model = model
		self.year = year
		self.odometer = 0

	def get_describe(self):
		long_name = str(self.year) + ' ' + self.make + ' ' + self.model
		return long_name

	def read_meter(self):
		print('this car has ' + str(self.odometer) + 'miles on it')

	def update_meter(self, miles):
		"""可以通过方法修改属性值"""
		self.odometer = miles

	def increment_odometer(self, miles):
		"""可以通过方法对属性的值进行递增"""
		self.odometer += miles

	def fill_gas_tank(self):
		print('汽车的油箱')

# my_car = Car('audi', 'a6', 2020)
# print(my_car.get_describe())






