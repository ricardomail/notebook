try:
	# 将字符串转化为float类型
	num1 = float(input('请输入数字：'))
	num2 = float(input('请输入数字：'))
	sum = num1 / num2
except ZeroDivisionError:
	print('不能除零')
else:
	# try模块中执行成功后走进else模块中
	print(sum)

# 类型转换 int('9') 可以转换的包括String类型和其他数字类型，但会丢失精度
# float(1) | float('1') 可以转换String和其他数字类型，不足的位数用0补齐，例如1会变成1.0
# str() 转化为String类型
# eval（Str）执行一个字符串表达式，返回计算的结果 eval('12+23') 35
# list() 将序列转化为一个列表，参数可以为元祖，字典，列表， 为字典时返回字典的key组成的集合
# tuple() 可以是元祖 列表或字典，为字典时返回字典的key组成的集合
# set()
# ord(x) 返回对应的ASCII数值， 或者Unicode数值
# hex(x) 把一个整数转换成十六进制字符串
# oct(x) 把一个整数转化为八进制的字符串
