# read excel

import xlrd
def read_excel(who):
	xlx = xlrd.open_workbook(who+'.xls')
	sheet1 = xlx.sheet_by_index(0)

	for i in range(sheet1.nrows):
		no = sheet1.cell(i,0).value
		name = sheet1.cell(i,1).value
		gender = sheet1.cell(i,2).value
		gender_id = None
		if gender == '男':
			gender_id = 1
		else:
			gender_id = 0
		card_id = sheet1.cell(i,3).value
		college = sheet1.cell(i,4).value
		college_id = None
		if college == "信息工程学院":
			college_id = 1
		elif college == '马克思主义研究学院':
			college_id = 2
		elif college == "新闻学院":
			college_id = 3
		elif college == "计算机学院":
			college_id = 4
		if who == 'student':
			grade = sheet1.cell(i,5).value
			grade_id = None
			if grade == "助教":
				grade_id = 1
			elif grade == "讲师":
				grade_id = 2
			elif grade == "副教授":
				grade_id = 3
			elif grade == "教授":
				grade_id = 4

		else:
			position = sheet1.cell(i,5).value
			position_id = None
			if position == "助教":
				position_id = 1
			elif position == "讲师":
				position_id = 2
			elif position == "副教授":
				position_id = 3
			elif position == "教授":
				position_id = 4

		tel = sheet1.cell(i,6).value
		eamil = sheet1.cell(i,7).value
		birth = sheet1.cell(i,8).value

		if who == "student":
			print('*'*100)
			print(i, no,name,gender_id,card_id,college_id,grade_id,tel,eamil,birth)
			print(i, no,name,gender,card_id,college,grade,tel,eamil,birth)
		else:
			print('*'*100)
			print(i, no,name,gender_id,card_id,college_id,position_id,tel,eamil,birth)
			print(i, no,name,gender,card_id,college,position,tel,eamil,birth)

if __name__ == '__main__':
	read_excel('student')
