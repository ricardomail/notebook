# 继承
from pyclass03 import Car

class ElectricCar(Car):
	"""电动车"""
	def __init__(self, make, model, year):
		super().__init__(make, model, year)
		# 子类中独有的属性
		self.battery_size = 70

	def describe_battery(self):
		"""子类中特有的方法"""
		print('this car has a ' + str(self.battery_size) + '-kwh battery')

	def fill_gas_tank(self):
		"""方法重写， 重写父类中的方法"""
		print('电动汽车没有油箱')

my_tesla = ElectricCar('tesla', 'model s', 2020)
# print(my_tesla.get_describe())
# my_tesla.describe_battery()
my_tesla.fill_gas_tank()
		