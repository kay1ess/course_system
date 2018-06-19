
import random
import string
import xlrd,xlwt
import os


def name_gen():
	name1 = ['赵','钱','孙','李','周','吴','郑','王','金','何','毛','宋','张','章','丁']
	name2 = ['','小','晓','佳','学','杰']
	name3 = ['凯','伦','杰','云','芸','辉','瑞','磊','俊','英','华','红','宏','洪','鸿','军','君','骏','茵','颖','莹','瑛']
	name = random.choice(name1)+random.choice(name2)+random.choice(name3)
	return name 

# No
def no_gen():
	no1 = ['2015','2016','2017','2018']
	no2 = '01'+random.choice(string.digits)+random.choice(string.digits)
	no3 = random.choice(string.digits)+random.choice(string.digits)+random.choice(string.digits)
	no = random.choice(no1)+no2+no3
	return no

def t_e_no_gen(x):
	if x == 'teacher':
		no1 = ['0100','0200','0300','0400']
	else:
		no1 = ['0990','0880']
	no2 = []
	for _ in range(4):
		no2.append(random.choice(string.digits))
	no = random.choice(no1) + ''.join(no2)
	return no

# CardID
def id_gen():
	id1 = []
	for _ in range(6):
		id1.append(random.choice(string.digits))
	id2 = '19' + str(random.randint(70,99))
	id3 = '200' + random.choice(string.digits)
	id4 = random.choice(['01','02','03','04','05','06','07','08','09','10','11','12']) + random.choice([random.choice(['01','02','03','04','05','06','07','08','09']),str(random.randint(10,31))])
	id5 = random.choice(string.digits)+random.choice(string.digits)+random.choice(string.digits)+random.choice(string.digits+'X')
	id_ = ''.join(id1) + random.choice([id2,id3]) + id4 + id5
	return id_

def t_e_id_gen():
	id1 = []
	for _ in range(6):
		id1.append(random.choice(string.digits))
	id2 = '19' + str(random.randint(50,86))
	id4 = random.choice(['01','02','03','04','05','06','07','08','09','10','11','12']) + random.choice([random.choice(['01','02','03','04','05','06','07','08','09']),str(random.randint(10,31))])
	id5 = random.choice(string.digits)+random.choice(string.digits)+random.choice(string.digits)+random.choice(string.digits+'X')
	id_ = ''.join(id1) + id2 + id4 + id5
	return id_
def t_e_birth_gen():
	return t_e_id_gen()[6:14]

# 学院
def college_gen():
	college = random.choice(['信息工程学院','新闻学院','计算机学院','马克思主义研究学院'])
	return college

# 年级
def grade_gen():
	no = ['2015','2016','2017','2018']
	grade = random.choice(no) + '级'
	return grade

# 性别
def gender_gen():
	gender = random.choice(['男', '女'])
	return gender

def  tel_gen():
	# 电话
	t1 = ['131','132','133','132','135','178','177','181','182','183','185','186']
	t2 = []
	for _ in range(8):
		t2.append(random.choice(string.digits))
	tel = random.choice(t1) + ''.join(t2)
	return tel

def email_gen():
	e1 = []
	e2 = ['qq.com','163.com','126.com','smg.cn','hotmail.com','yahoo.com.cn']
	for i in range(random.randint(6,10)):
		e1.append(random.choice([random.choice(string.digits),random.choice(string.ascii_letters)]))
	email = ''.join(e1) + '@' +random.choice(e2)
	return email

def birth_gen():
	id_ = id_gen()
	return id_[6:14]

def positon_gen():
	p1 = ['助教','讲师','副教授','教授']
	positon = random.choice(p1)
	return positon

def student_excel(p):
	workbook = xlwt.Workbook(encoding='utf-8')
	worksheet = workbook.add_sheet('Student_Sheet')
	row0 = ['学号','姓名','性别','身份证','学院','年级','电话','电子邮件','生日']
	for j in range(0,len(row0)):
		worksheet.write(0,j,row0[j])
	for i in range(1,p):
			worksheet.write(i,0, label=no_gen())
			worksheet.write(i,1, label=name_gen())
			worksheet.write(i,2, label=gender_gen())
			worksheet.write(i,3, label=id_gen())
			worksheet.write(i,4, label=college_gen())
			worksheet.write(i,5, label=grade_gen())
			worksheet.write(i,6, label=tel_gen())
			worksheet.write(i,7, label=email_gen())
			worksheet.write(i,8, label=birth_gen())
	workbook.save('student.xls')

def t_e_excel(t_e,p):
	workbook = xlwt.Workbook(encoding='utf-8')
	worksheet = workbook.add_sheet(t_e+'Sheet')
	row0 = ['学号','姓名','性别','身份证','学院','职位','电话','电子邮件','生日']
	for j in range(0,len(row0)):
		worksheet.write(0,j,row0[j])
	for i in range(1,p):
			worksheet.write(i,0, label=t_e_no_gen(t_e))
			worksheet.write(i,1, label=name_gen())
			worksheet.write(i,2, label=gender_gen())
			worksheet.write(i,3, label=t_e_id_gen())
			worksheet.write(i,4, label=college_gen())
			worksheet.write(i,5, label=positon_gen())
			worksheet.write(i,6, label=tel_gen())
			worksheet.write(i,7, label=email_gen())
			worksheet.write(i,8, label=t_e_birth_gen())
	workbook.save(t_e+'.xls')



if __name__ == '__main__':

	student_excel(1000);
	t_e_excel('teacher',10)
	t_e_excel('edu',3)
	print('Done!')
