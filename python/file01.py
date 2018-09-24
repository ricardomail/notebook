# 打开文件，读取文件全部内容
# with open('pi_digits.txt') as f:
# 	contents = f.read()
# 	print(contents)

# 写入文件 
# a 附加模式。w 写入模式。r 读取模式。 r+ 读写模式
with open('pi_digits.txt', 'a') as f2:
	f2.write('I love pie')

	#读取所有内容并按照行形成列表
	contents = f2.readlines()
	print(contents)