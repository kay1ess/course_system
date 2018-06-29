import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from course.ulti import MyPagination
from edu.models import NewCourse, News
from teacher.form import AppForm
from teacher.models import AppliedCourse, AppliedCourse_Pos_Ti, Teacher
from teacher.models import Classroom,Weeks,Times
from edu.models import NewCourse
import datetime
# Create your views here.

# 自定义装饰器 用来检测访问教师视图的的权限

def check_group2(user):
    g_name = user.groups.all().first()
    g_id = Group.objects.filter(name=g_name).first().id
    return (True if g_id==2 else False)


@login_required
@user_passes_test(check_group2)
def index(request):
    t_id = Teacher.objects.filter(no__username=request.user).first().id
    today_ = datetime.datetime.now().weekday()+1
    today_courses = AppliedCourse.objects.filter(choose=True, teacher_id=t_id, week_id=today_)
    news = News.objects.filter(Q(watchers='1')|Q(watchers='2')).order_by("-m_time","-c_time")[:5]
    return render(request, "t_index.html", {"today_course":today_courses, "news":news})

@login_required
@user_passes_test(check_group2)
def app_course(request):
    if request.method == "GET":
        obj = AppForm()
        courses = NewCourse.objects.filter(status=0,is_applied=False).order_by('-ctime')
        obj2 = MyPagination(courses.count(), request.GET.get('p'), 10, url='appCourse.html')
        courses = courses[obj2.start():obj2.end()]
        return render(request, "t_appCourse.html", {"courses":courses,"obj":obj, "obj2":obj2})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        obj = AppForm(request.POST)
        teacher_id = Teacher.objects.filter(no__username=request.user).first().id
        if obj.is_valid():
            try:
                with transaction.atomic():
                    AppliedCourse.objects.create(
                        no=obj.cleaned_data.get("no"),
                        name=obj.cleaned_data.get("name"),
                        college_id=obj.cleaned_data.get("college_id"),
                        credit=obj.cleaned_data.get("credit"),
                        classroom_id=obj.cleaned_data.get("classroom_id"),
                        week_id=obj.cleaned_data.get("week_id"),
                        time_id=obj.cleaned_data.get("time_id"),
                        teacher_id=teacher_id
                    )

                    AppliedCourse_Pos_Ti.objects.create(
                        classroom_id=obj.cleaned_data.get("classroom_id"),
                        week_id=obj.cleaned_data.get("week_id"),
                        time_id=obj.cleaned_data.get("time_id"),
                        applied_course_id=AppliedCourse.objects.last().id,
                        teacher_id=teacher_id
                                                        )
                    NewCourse.objects.filter(no=obj.cleaned_data.get("no")).update(status=1)
                    print(obj.cleaned_data.get("no")+"申请成功")
                    ret["msg"] = "申请成功"
            except Exception as e:
                print(str(e))
                if str(e) == "UNIQUE constraint failed: teacher_appliedcourse_pos_ti.classroom_id, teacher_appliedcourse_pos_ti.time_id, teacher_appliedcourse_pos_ti.week_id":
                    ret["status"] = False
                    ret["msg"] = "该教室已被使用，请另选择时间段或教室"
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = False
            ret["msg"] = "申请数据有误，请重新尝试"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_group2)
def applied_course(request):
    t_id = Teacher.objects.filter(no__username=request.user).first().id
    applied_course_list = AppliedCourse.objects.filter(teacher_id=t_id).order_by("-applied_time")
    return render(request, "t_appliedCourse.html", {"applied_course_list":applied_course_list})

@login_required
@user_passes_test(check_group2)
def teach_plan(request):
    t_id = Teacher.objects.filter(no__username=request.user).first().id
    cour = AppliedCourse.objects.filter(choose=True,teacher_id=t_id)
    weeks = Weeks.objects.all()
    times = Times.objects.all()
    return render(request, "t_teachPlan.html", locals())

@login_required
@user_passes_test(check_group2)
def info(request):
    teacher = Teacher.objects.get(no__username=request.user)
    return render(request, "t_info.html", {"teacher": teacher})


@login_required
@user_passes_test(check_group2)
def editTeacher(request):

    if request.method == "POST":
        ret = {"status": True, "msg": None}
        print(request.POST)
        no = request.POST.get("no")
        try:
            Teacher.objects.filter(no__username=no).update(
                tel=request.POST.get("tel"),
                email=request.POST.get("email")
            )
            ret["msg"] = "修改成功"
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "修改失败"
        return HttpResponse(json.dumps(ret, ensure_ascii=False))

