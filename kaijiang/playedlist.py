#!/usr/bin/python
#coding:UTF-8
import itertools

#复式算法
#@params bet		投注列表：123,45,2,59,789
#@params data		开奖所需的那几个：4,5,0,8,2
#@return 			返回中奖注数
def multiple(bet, data):
	ls = bet.split(",")
	betlist = []
	for val in ls:
		betlist.append(list(val))
	#采用笛卡尔乘积算法 枚举出该投注列表的所有组合 一一比较
	count = 0
	for x in itertools.product(*betlist):
		no = ",".join(list(x))
		if(no == data):
			count+=1
	return count


#单式算法
#@params bet		投注列表：1,5,2,9,2|3,2,4,6,4
#@params data		开奖所需的那几位号码：4,5,3,6,8
#@return			返回中奖注数
def single(bet, data):
	ls = bet.split("|")
	count = 0
	for x in ls:
		if(x == data):
			count+=1
	return count

#两个列表，返回包含相同数字的个数(列表中不能有重复数据)
def listCompare(a, b):
	count = 0
	for i in range(len(a)):
		isMatch = False
		for j in range(len(b)):
			if(a[i] == b[j]):
				isMatch = True
		if(isMatch):
			count+=1
	return count

#匹配参数
#count表示重号个数 Max表示重号最大出现次数
def match(a, count, Max):
	b = []
	num = 0
	for x in a:
		if(a.count(x) > 1):
			b.append(x)
			if(a.count(x) > num):
				num = a.count(x)
	c = list(set(b))
	if(count == 0 and count == len(c)):
		return True
	if(count != len(c) or num != Max):
		return False
	return True

#拆分列表中的重号
#[0]:单号 [1]:二重号 [2]:三重号码 [3]:四重号码 [4]:五重号码
def splitList(a):
	sing = []
	mult2 = []
	mult3 = []
	mult4 = []
	mult5 = []
	for x in a:
		if(a.count(x) == 1):
			sing.append(x)
		elif(a.count(x) == 2):
			mult2.append(x)
		elif(a.count(x) == 3):
			mult3.append(x)
		elif(a.count(x) == 4):
			mult4.append(x)
		elif(a.count(x) == 5):
			mult5.append(x)
	ls = []
	ls.append(sing)
	ls.append(mult2)
	ls.append(mult3)
	ls.append(mult4)
	ls.append(mult5)
	return ls

#5星复式
def dxwf5f(bet, data):
	count = multiple(bet,data)
	return count
	
#5星单式
def dxwf5d(bet, data):
	count = single(bet, data)
	return count

#5星组选120
def dxwf5z120(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,0,0) != True):#开奖号码不能有重号
		return 0
	count = 0
	if(listCompare(a,b) == 5):
		count = 1
	return count

#5星组选60
def dxwf5z60(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,1,2) != True):#开奖号码必须有一个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[1]) == 1):#比较二重号
		if(listCompare(list(a[1]),c[0]) == 3):#比较单号
			count = 1
	return count

#5星组选30
def dxwf5z30(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,2,2) != True):#开奖号码必须有两个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[1]) == 2):#比较二重号
		if(listCompare(list(a[1]),c[0]) == 1):#比较单号
			count = 1
	return count

#5星组选20
def dxwf5z20(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,1,3) != True):#开奖号码必须有一个三重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[2]) == 1):#比较三重号
		if(listCompare(list(a[1]),c[0]) == 2):#比较单号
			count = 1
	return count

#5星组选10
def dxwf5z10(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,2,3) != True):#开奖号码必须有一个三重号和一个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[2]) == 1):#比较三重号
		if(listCompare(list(a[1]),c[1]) == 1):#比较二重号
			count = 1
	return count

#5星组选5
def dxwf5z5(bet, data):
	a = bet.split(",")
	b = data.split(",")
	if(match(b,1,4) != True):#开奖号码必须有一个四重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[3]) == 1):#比较四重号
		if(listCompare(list(a[1]),c[0]) == 1):#比较单号
			count = 1
	return count

#4星前四复式
def dxwfQ4f(bet, data):
	a = data.split(",")
	del a[4]
	b = ",".join(a)
	count = multiple(bet,b)
	return count

#4星前四单式
def dxwfQ4d(bet, data):
	a = data.split(",")
	del a[4]
	b = ",".join(a)
	count = single(bet,b)
	return count

#4星后四复式
def dxwfH4f(bet, data):
	a = data.split(",")
	del a[0]
	b = ",".join(a)
	count = multiple(bet,b)
	return count

#4星后四单式
def dxwfH4d(bet, data):
	a = data.split(",")
	del a[0]
	b = ",".join(a)
	count = single(bet,b)
	return count

#4星组选24
def dxwf4z24(bet, data):
	a = bet.split(",")
	b = data.split(",")
	del b[0]
	if(match(b,0,0) != True):#开奖号码不能有重号
		return 0
	count = 0
	if(listCompare(a,b) == 4):
		count = 1
	return count

#4星组选12
def dxwf4z12(bet, data):
	a = bet.split(",")
	b = data.split(",")
	del b[0]
	if(match(b,1,2) != True):#开奖号码必须有一个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[1]) == 1):#比较二重号
		if(listCompare(list(a[1]),c[0]) == 2):#比较单号
			count = 1
	return count

#4星组选6
def dxwf4z6(bet, data):
	a = bet.split(",")
	b = data.split(",")
	del b[0]
	if(match(b,2,2) != True):#开奖号码必须有两个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(a,c[1]) == 2):#比较二重号
		count = 1
	return count


#4星组选4
def dxwf4z4(bet, data):
	a = bet.split(",")
	b = data.split(",")
	del b[0]
	if(match(b,1,3) != True):#开奖号码必须有一个三重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(list(a[0]),c[2]) == 1):#比较三重号
		if(listCompare(list(a[1]),c[0]) == 1):#比较单号
			count = 1
	return count


#3星前三复式
def sxwfQ3f(bet, data):
	a = data.split(",")
	del a[4]
	del a[3]
	b = ",".join(a)
	count = multiple(bet,b)
	return count

#3星前三单式
def sxwfQ3d(bet, data):
	a = data.split(",")
	del a[4]
	del a[3]
	b = ",".join(a)
	count = single(bet,b)
	return count

#3星中三复式
def sxwfz3fs(bet, data):
	a = data.split(",")
	del a[4]
	del a[0]
	b = ",".join(a)
	count = multiple(bet,b)
	return count

#3星中三单式
def sxwfz3ds(bet, data):
	a = data.split(",")
	del a[4]
	del a[0]
	b = ",".join(a)
	count = single(bet,b)
	return count

#3星后三复式
def sxwfH3f(bet, data):
	a = data.split(",")
	del a[0]
	del a[0]
	b = ",".join(a)
	count = multiple(bet,b)
	return count

#3星后三单式
def sxwfH3d(bet, data):
	a = data.split(",")
	del a[0]
	del a[0]
	b = ",".join(a)
	count = single(bet,b)
	return count

#3星后三和值尾数
def sxh3hzws(bet, data):
	a = bet.split(" ")
	b = data.split(",")
	del b[0]
	del b[0]
	num = int(b[0])+int(b[1])+int(b[2])
	last = num
	if(num > 10):
		last = num%10
	c = [str(last)]
	count = 0
	if(listCompare(a,c) == 1):
		count = 1
	return count

#3星前三组三
def sxzxQ3z3(bet, data):
	a = list(bet)
	b = data.split(",")
	del b[4]
	del b[3]
	if(match(b,1,2) != True):#开奖号码必须有一个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(a,c[1]) == 1):#比较二重号
		if(listCompare(a,c[0]) == 1):#比较单号
			count = 1
	return count

#3星前三组六
def sxzxQ3z6(bet, data):
	a = list(bet)
	b = data.split(",")
	del b[4]
	del b[3]
	if(match(b,0,0) != True):#开奖号码不能有重号
		return 0
	count = 0
	if(listCompare(a,b) == 3):
		count = 1
	return count

#3星中三组三
def sxzxz3z3(bet, data):
	a = list(bet)
	b = data.split(",")
	del b[4]
	del b[0]
	if(match(b,1,2) != True):#开奖号码必须有一个二重号
		return 0
	c = splitList(b)
	count = 0
	if(listCompare(a,c[1]) == 1):#比较二重号
		if(listCompare(a,c[0]) == 1):#比较单号
			count = 1
	return count


// 中三组六
exports.sxzxz3z6














G_PLAYED_PRO = {} #玩法列表 全局使用
G_PLAYED_PRO['dxwf5f'] = dxwf5f
G_PLAYED_PRO['dxwf5d'] = dxwf5d
G_PLAYED_PRO['dxwf5z120'] = dxwf5z120
G_PLAYED_PRO['dxwf5z60'] = dxwf5z60
G_PLAYED_PRO['dxwf5z30'] = dxwf5z30
G_PLAYED_PRO['dxwf5z20'] = dxwf5z20
G_PLAYED_PRO['dxwf5z10'] = dxwf5z10
G_PLAYED_PRO['dxwf5z5'] = dxwf5z5
G_PLAYED_PRO['dxwfQ4f'] = dxwfQ4f
G_PLAYED_PRO['dxwfQ4d'] = dxwfQ4d
G_PLAYED_PRO['dxwfH4f'] = dxwfH4f
G_PLAYED_PRO['dxwfH4d'] = dxwfH4d











