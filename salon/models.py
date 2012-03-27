#encoding=utf-8
from django.db import models
import datetime

# Create your models here.
class Salon(models.Model):
	#主键
	salon_id = models.AutoField(primary_key = True)

	#沙龙对应的编码（用于在url中显示沙龙相关信息）
	code = models.CharField(max_length = 40)
	#活动名称
	name = models.CharField(max_length = 100)
	#开始时间
	start_time = models.DateTimeField()
	#结束时间
	end_time = models.DateTimeField()
	#活动创建人
	creator = models.CharField(max_length = 40)
	#活动描述
	description = models.CharField(max_length = 200)
	#活动地址
	address = models.CharField(max_length = 200)

	def is_finished(self):
		return self.end_time < datetime.datetime.today()
	def is_not_start(self):
		return self.start_time > datetime.datetime.today()
	def is_active(self):
		return self.start_time < datetime.datetime.today() < self.end_time

	def get_status(self):
		if (self.is_finished()):
			return 'finished'
		elif (self.is_not_start()):
			return 'not-start'
		elif (self.is_active()):
			return 'active'
		else:
			return 'unknown'

	def __unicode__(self):
		return "%s" % (self.name)

class User(models.Model):
	#主键
	user_id = models.AutoField(primary_key = True)
	#外键，关联salon
	salon = models.ForeignKey(Salon)
	#姓名
	name = models.CharField(max_length = 40) 
	#手机号
	mobile = models.CharField(null=True, max_length = 11)
	#邮件
	email = models.EmailField()	
	#公司名
	company = models.CharField(null=True, max_length = 100) 
	#自我介绍
	introduction = models.CharField(null=True, max_length = 200) 
	# 注册时间
	register_time = models.DateTimeField()

	#处理状态
	# 1、是否以删除 	0:否 1:是  
	# 2、已接受状态 	0:为处理 1:已接受 2:已拒绝 
	# 3、是否已发邮件 	0:否 1:是
	# 4、是否已签到  	0:否 1:是  
	# 5、是否线下注册 	0:否 1:是  
	status = models.CharField(default="00000", max_length = 20) 
	
	#二维码
	barcode = models.CharField(null = True, max_length = 40) 
	
	def __unicode__(self):
		return "%s(from %s), %s, %s, %s" % (self.name, self.company, self.mobile, self.email, self.introduction)

	def __getattr__(self,name):
		if name=='checkined':
			return self.get_flag(4)
		elif name=='accepted':
			return self.get_flag(2)
		elif name == 'mailed':
			return self.get_flag(3)
		elif name == 'offline_reg':
			return self.get_flag(5)
		elif name == 'deleted':
			return self.get_flag(1)
		else:
			return object.__getattr__(self,name)

	def __setattr__(self,name,value):
		if name=='checkined':
			self.set_flag(4,value) 		
		elif name=='accepted':
			self.set_flag(2,value)
		elif name == 'mailed':
			self.set_flag(3,value)
		elif name == 'offline_reg':
			self.set_flag(5,value)
		elif name == 'deleted':
			self.set_flag(1,value)
		else:
			object.__setattr__(self,name,value)

	def get_flag(self,index):
		return int(self.status[index-1])

	def set_flag(self,index,value):
		temp = self.status
		head = temp[:index-1]
		rear = temp[index:]	
		#print 'head:'+head,'rear:'+rear
		self.status =head+str(value)+rear
		self.save()

	@classmethod
	def get_untreated(cls, salon_id):
		temp = cls.objects.filter(salon = salon_id)
		users = []
		for user in temp:
			if user.accepted == 0:
				users.append(user)
		return users

	@classmethod
	def get_accepted(cls, salon_id):
		temp = cls.objects.filter(salon = salon_id)
		users = []
		for user in temp:
			if user.accepted == 1:
				users.append(user)
		return users

	@classmethod
	def get_rejected(cls, salon_id):
		temp = cls.objects.filter(salon = salon_id)
		users = []
		for user in temp:
			if user.accepted == 2:
				users.append(user)
		return users
