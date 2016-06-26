#!/usr/bin/python
#coding:UTF-8
import HTMLParser
import urllib2
import time
import datetime
import mysql.connector
import re
import traceback
from playedlist import *

G_ENCRYPT_KEY="39d8b1e2372e39850bb51d63416784d5";

#类名:MySQLdb
#描述:MYSQL数据库连接器
#引擎:mysql.connector
class MySQLdb:
	def __init__(self,config):
		self.config = config
		self.connector = self.connection()

	def connection(self):
		try:
			return mysql.connector.connect(**self.config)
		except Exception, e:
			print("连接数据库错误")
			raise e

	def select(self,sql):
		cursor = self.connector.cursor()
		try:
			cursor.execute(sql)
			result = cursor.fetchall()
			dataset = []
			if(result):
				for res in result:
					i = 0
					data = {}
					for field_desc in cursor.description:
						data[field_desc[0]] = res[i]
						i+=1
					dataset.append(data)
			return dataset
		except Exception, e:
			print("查询数据出错")
			raise e
		finally:
			cursor.close()

	def modify(self,sql):
		cursor = self.connector.cursor()
		try:
			cursor.execute(sql)
			result = self.connector.commit()
			return result
		except Exception, e:
			print("修改数据出错")
			raise e
		finally:
			cursor.close()

	def modify_multiple(self,sqls):
		cursor = self.connector.cursor()
		try:
			for sql in sqls:
				cursor.execute(sql)
			result = self.connector.commit()
			return result
		except Exception, e:
			print("修改数据出错")
			raise e
		finally:
			cursor.close()

	def __del__(self):
		self.connector.close()

#本地数据库配置信息
config = {
	"host":"127.0.0.1",
	"user":"root",
	"password":"",
	"port":3306,
	"database":"xy_yule",
	"charset":"utf8"
}
G_MYSQL = MySQLdb(config) #MySQLdb对象 全局使用

#读取所有的玩法列表
sql = "select id,ruleFun from xy_played"
DataSet = G_MYSQL.select(sql)
G_PLAYED = {} #玩法列表 全局使用
if DataSet:
	for row in DataSet:
		G_PLAYED[row['id']] = row['ruleFun']

#类名:CQSSC_by_CP360_Parser
#描述:重庆时时彩开奖器 数据采自360彩票网
class CQSSC_by_CP360_Parser(HTMLParser.HTMLParser):
	def __init__(self,_mysql):
		HTMLParser.HTMLParser.__init__(self)
		self.mysql = _mysql #数据库连接池
		self.type = 1 #彩种类型 1:表示重庆时时彩
		self.time = "" #数据采集时间
		self.date = "" #期号
		self.lastdate = "" #最近一次开奖期号
		self.number = "" #开奖号码
		self.isDate = False #是否是开奖期号
		self.isNumber = False #是否是开奖号码
		self.timeout = 30 #超时时间
		self.url = "http://cp.360.cn/ssccq" #开机数据采集地址
		self.req_header = { #伪装http请求头Chrome/51.0.2704.84
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Language":"zh-CN,zh;q=0.8",
			"Cache-Control":"max-age=0",
			"Connection":"keep-alive",
			"Host":"cp.360.cn",
			"If-Modified-Since":"Thu, 16 Jun 2016 12:06:05 GMT",
			"Upgrade-Insecure-Requests":1,
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
		}
		self.header = {
			"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)"
		}
		#重庆时时彩开奖时间列表
		self.timeconf=["00:05", "00:10", "00:15", "00:20", "00:25", "00:30", "00:35", "00:40", "00:45", "00:50", "00:55", "01:00", "01:05", "01:10", "01:15", "01:20", "01:25", "01:30", "01:35", "01:40", "01:45", "01:50", "01:55", "10:00", "10:10", "10:20", "10:30", "10:40", "10:50", "11:00", "11:10", "11:20", "11:30", "11:40", "11:50", "12:00", "12:10", "12:20", "12:30", "12:40", "12:50", "13:00", "13:10", "13:20", "13:30", "13:40", "13:50", "14:00", "14:10", "14:20", "14:30", "14:40", "14:50", "15:00", "15:10", "15:20", "15:30", "15:40", "15:50", "16:00", "16:10", "16:20", "16:30", "16:40", "16:50", "17:00", "17:10", "17:20", "17:30", "17:40", "17:50", "18:00", "18:10", "18:20", "18:30", "18:40", "18:50", "19:00", "19:10", "19:20", "19:30", "19:40", "19:50", "20:00", "20:10", "20:20", "20:30", "20:40", "20:50", "21:00", "21:10", "21:20", "21:30", "21:40", "21:50", "22:00", "22:05", "22:10", "22:15", "22:20", "22:25", "22:30", "22:35", "22:40", "22:45", "22:50", "22:55", "23:00", "23:05", "23:10", "23:15", "23:20", "23:25", "23:30", "23:35", "23:40", "23:45", "23:50", "23:55", "00:00"]

	#HTMLParser回调函数
	#解析号码标签头
	def handle_starttag(self,tag,attrs):
		if(tag == "em"):
			self.isDate = True
		elif(tag == "li"):
			for(name,value) in attrs:
				if(name == "class" and value == "ico-ball3"):
					self.isNumber = True

	#HTMLParser回调函数
	#获取号码数据
	def handle_data(self,data):
		if(self.isDate):
			self.date = time.strftime('%Y%m%d-',time.localtime())+data[len(data)-3:len(data)]
		elif(self.isNumber):
			self.number = data if(len(self.number) == 0) else self.number+','+data

	#HTMLParser回调函数
	#解析号码标签尾
	def handle_endtag(self, tag):
		if(tag == "em"):
			self.isDate = False
		elif(tag == "li"):
			self.isNumber = False

	#计算当前时间距离下一期开奖时间的秒数
	def time_difference(self):
		actionNo = int(self.date[9:12])
		if(actionNo > 120):
			actionNo = 120
		times = self.timeconf[actionNo].split(':')#这里的actionNo其实是下一期期号 因为时间列表下标从0开始
		timeStr = time.strftime("%Y-%m-%d {0}:{1}:%S".format(times[0],times[1]))

		curTime = time.localtime()
		nexTime = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")

		curDtTime = datetime.datetime(*curTime[:6])
		nexDtTime = datetime.datetime(*nexTime[:6])
		diffDtTime = nexDtTime - curDtTime
		return (diffDtTime).seconds

	#结算本彩种所有投注
	def settlement(self):
		try:
			#写入本期开奖数据
			sql = "insert into xy_data(type,time,number,data) values({0},{1},'{2}','{3}')".format(self.type,time.time(),self.date,self.number)
			self.mysql.modify(sql)
			#读取本期开奖投注数据
			sql = "select id,playedId,actionData,weiShu,actionName,type from xy_bets where isDelete=0 and type={0} and actionNo='{1}'".format(self.type,self.date)
			bets = self.mysql.select(sql)
			if(bets):
				sqls = []
				for bet in bets:
					zjCount = 0 #中奖注数
					if(bet['type'] == 34):
						pass#...........
					else:
						funpro = G_PLAYED_PRO[G_PLAYED[bet['playedId']]]
						if(funpro):
							zjCount = funpro(bet['actionData'],self.number)#调用相关规则玩法的函数 返回该玩法中奖注数
						else:
							print('该玩法没有匹配相关函数')
					sqls.append("call kanJiang({0},{1},'{2}','{3}')".format(bet['id'],zjCount,self.number,"QQ:421991377-"+G_ENCRYPT_KEY))
				self.mysql.modify_multiple(sqls)#执行存储过程
			return len(bets)
		except Exception, e:
			raise e

	#开始任务
	def start(self):
		while(True):
			self.time = time.strftime('%Y-%m-%d %H:%M:%S')
			self.date = ''
			self.number = ''
			print('开始从360彩票网抓取重庆时时彩数据')
			try:
				request = urllib2.Request(self.url,None,self.header)
				print('正在打开网址'+self.url)
				response = urllib2.urlopen(request,None,self.timeout)
				print('正在读取HTML内容...')
				htmlValue = response.read()
				response.close()
			except Exception, e:
				print '打开网址超时5秒后重启打开'
				time.sleep(5)
				continue

			print('解析HTML数据')
			try:
				pass
				if(len(htmlValue)>0):
					#解析期号所在段落
					em_beg = htmlValue.find('<em class="red" id="open_issue">')
					em_end = htmlValue.find('</em>',em_beg)
					em_text = htmlValue[em_beg:em_end+len('</em>')]
					self.feed(em_text)

					#解析号码所在段落
					div_beg = htmlValue.find('<div class="ball-num clearfix">')
					div_end = htmlValue.find('</div>',div_beg)
					div_text = htmlValue[div_beg:div_end+len('</div>')]
					self.feed(div_text)
			except Exception, e:
				print '数据解析失败5秒后重新采集'
				time.sleep(5)
				continue

			if(self.number == '?,?,?,?,?'):
				print('开机进行中...20秒后重新抓取数据')
				time.sleep(20)
				continue

			if(self.date == self.lastdate):
				print('未到开奖时间10秒后重试')
				time.sleep(10)
				continue
			else:
				self.lastdate = self.date

			try:
				num = self.settlement()#结算本期开奖投注数据
				if(num > 0):
					print('重庆时时彩第'+self.date+'期投注结算完成')
				else:
					print('重庆时时彩第'+self.date+'期没有人投注')
			except Exception, e:
				print('重庆时时彩第'+self.date+'期投注结算失败')
				print e
			
			difftime = self.time_difference()
			print('重庆时时彩 本期期号'+self.date+' 本期开奖号码:'+self.number)
			print('数据采集完成'+str(difftime)+'秒后采集下一期数据')
			time.sleep(difftime)







#cqssc = CQSSC_by_CP360_Parser(G_MYSQL)
#cqssc.start()


a = "253"
b = "2,5,3,3,3"
c = sxzxQ3z6(a,b)
print c













del G_MYSQL


