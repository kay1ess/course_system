import json

from django.http import HttpResponse
from django.shortcuts import render
from edu.models import NewCourse
from teacher.form import AppForm
from teacher.models import AppliedCourse, AppliedCourse_Pos_Ti
from teacher.models import Classroom,Weeks,Times
from edu.models import NewCourse
import datetime
# Create your views here.


def index(request):
    today_ = datetime.datetime.now().weekday()+1
    today_courses = AppliedCourse.objects.filter(week_id=1)
    return render(request, "t_index.html", {"today_course":today_courses})

def app_course(request):
    if request.method == "GET":
        obj = AppForm()
        courses = NewCourse.objects.filter(status=None).order_by('-ctime')
        return render(request, "t_appCourse.html", {"courses":courses, "obj":obj})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        obj = AppForm(request.POST)
        if obj.is_valid():
            try:
                AppliedCourse.objects.create(
                    no=obj.cleaned_data.get("no"),
                    name=obj.cleaned_data.get("name"),
                    college_id=obj.cleaned_data.get("college_id"),
                    credit=obj.cleaned_data.get("credit"),
                    classroom_id=obj.cleaned_data.get("classroom_id"),
                    week_id=obj.cleaned_data.get("week_id"),
                    time_id=obj.cleaned_data.get("time_id"),
                )
                AppliedCourse_Pos_Ti.objects.create(
                    classroom_id=obj.cleaned_data.get("classroom_id"),
                    week_id=obj.cleaned_data.get("week_id"),
                    time_id=obj.cleaned_data.get("time_id"),
                    applied_course_id=AppliedCourse.objects.last().id
                                                    )
                NewCourse.objects.filter(no=obj.cleaned_data.get("no")).update(status=True)
                ret["msg"] = "申请成功"
            except Exception as e:
                    ret["status"] = False
                    ret["msg"] = "数据库写入异常，请联系管理员，错误代码："+str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = "申请数据有误，请重新尝试"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))



def applied_course(request):
    applied_course_list = AppliedCourse.objects.all().order_by("-applied_time")
    return render(request, "t_appliedCourse.html", {"applied_course_list":applied_course_list})

def teach_plan(request):
    pass

def info(request):
    pass

