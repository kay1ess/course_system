
import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.contrib.auth.models import User
from django.shortcuts import render

from edu.models import NewCourse, EduAdmin
from edu.views import check_group3
from patch.read_excel import read_excel_student, read_excel_teacher, read_excel_course
from student.models import Student
from teacher.models import Teacher


BASE_PATH = os.path.abspath('.')



@login_required
@user_passes_test(check_group3)
def course_excel_download(request):

	the_file_name = 'course_example.xls'
	path = os.path.join(os.path.join(BASE_PATH, 'static'), 'file')
	file = open(path + '/'+ the_file_name, 'rb')

	response = FileResponse(file)
	response["Content-Type"] = "application/octet-stream"
	response["Content-Disposition"] = "attachment;filename='course_example.xls'"
	return response

@login_required
@user_passes_test(check_group3)
def teacher_excel_download(request):
	the_file_name = 'teacher_example.xls'
	path = os.path.join(os.path.join(BASE_PATH, 'static'), 'file')
	file = open(path + '/' + the_file_name, 'rb')
	response = FileResponse(file)
	response["Content-Type"] = "application/octet-stream"
	response["Content-Disposition"] = "attachment;filename='teacher_example.xls'"
	return response

@login_required
@user_passes_test(check_group3)
def student_excel_download(request):
	the_file_name = 'student_example.xls'
	path = os.path.join(os.path.join(BASE_PATH, 'static'), 'file')
	file = open(path + '/' + the_file_name, 'rb')
	response = FileResponse(file)
	response["Content-Type"] = "application/octet-stream"
	response["Content-Disposition"] = "attachment;filename='student_example.xls'"
	return response

@login_required
@user_passes_test(check_group3)
def patch_add_student(request):
	file_obj = request.FILES.get('file')

	if file_obj:   # 处理附件上传到方法

		with open(os.path.join(os.path.join(BASE_PATH, 'media'), 'files') + file_obj.name, 'wb') as f:
			for line in file_obj.chunks():
				f.write(line)
		f.close()

		info = read_excel_student(os.path.join(os.path.join(BASE_PATH, 'media'), 'files') + file_obj.name)
		for i in info:
			try:
				User.objects.create_user(
					username=i[1],
					password=(i[4][12:18])
				)

				user = User.objects.last()
				no_id = user.id
				Student.objects.create(
					no_id=no_id,
					name=i[2],
					gender=i[3],
					card_id=i[4],
					college_id=i[5],
					grade_id=i[6],
					tel=i[7],
					email=i[8],
					birth=i[4][6:14]
				)
				user.groups.add(1)
			except Exception as e:
				print(str(e))
				return HttpResponse(("数据库写入失败，请检查是否有重复学号，或身份证号，错误代码:%s" % str(e)))
	return render(request, "manage_center.html")

@login_required
@user_passes_test(check_group3)
def patch_add_teacher(request):
	file_obj = request.FILES.get('file')

	if file_obj:   # 处理附件上传到方法

		with open(os.path.join(BASE_PATH+'/'+'media', 'files') + file_obj.name, 'wb') as f:
			for line in file_obj.chunks():
				f.write(line)
		f.close()

		info = read_excel_teacher(os.path.join(BASE_PATH+'/'+'media', 'files') + file_obj.name)
		for i in info:
			try:
				User.objects.create_user(
					username=i[1],
					password=(i[4][12:18])
				)

				user = User.objects.last()
				no_id = user.id
				Teacher.objects.create(
					no_id=no_id,
					name=i[2],
					gender=i[3],
					card_id=i[4],
					college_id=i[5],
					position_id=i[6],
					tel=i[7],
					email=i[8],
					birth=i[4][6:14]
				)
				user.groups.add(2)
			except Exception as e:
				print(str(e))
				return HttpResponse(("数据库写入失败，请检查是否有重复工号或身份证号，错误代码:%s" % str(e)))
	return render(request, "manage_center.html")

@login_required
@user_passes_test(check_group3)
def patch_add_course(request):
	file_obj = request.FILES.get('file')

	if file_obj:  # 处理附件上传到方法

		with open(os.path.join(BASE_PATH + '/' + 'media', 'files') + file_obj.name, 'wb') as f:
			for line in file_obj.chunks():
				f.write(line)
		f.close()

		info = read_excel_course(os.path.join(BASE_PATH + '/' + 'media', 'files') + file_obj.name)
		for i in info:
			try:
				NewCourse.objects.create(
					no=i[1],
					name=i[2],
					credit=i[3],
					college_id=i[4],
					created_by=EduAdmin.objects.get(no__username=request.user)
				)
			except Exception as e:
				print(str(e))
				return HttpResponse(("数据库写入失败，请检查是否有重复工号或身份证号，错误代码:%s" % str(e)))
	return render(request, "manage_center.html")
