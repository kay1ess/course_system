import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from teacher.models import AppliedCourse
from student.models import Selected
# Create your views here.
def index(request):
    return render(request, "s_index.html")

def select(request):
    courses = AppliedCourse.objects.filter(~Q(choose=True),status=True)
    return render(request, "s_select.html", {"courses":courses})

def selected(request):
    courses = Selected.objects.all()
    return render(request, "s_selected.html", {"courses":courses})

def courses(request):
    return render(request, "s_courses.html")

def info(request):
    pass

def choosed(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "选课成功！"}
        try:

            Selected.objects.create(
                # 用户还未登记
                no=request.POST.get("no"),
                name=request.POST.get("name"),
                college_id=request.POST.get("college"),
                # teacher_id=request.POST.get("teacher"),
                credit=request.POST.get("credit"),
                a_time_id=request.POST.get("time"),
                a_week_id=request.POST.get("week"),
                classroom_id=request.POST.get("classroom")
            )

            AppliedCourse.objects.filter(no=request.POST.get("no")).update(
                choose=True
            )

        except Exception as e:
            print(e)
            ret["status"] = False
            ret["msg"] = "数据库操作失败，请联系系统管理员"
    return HttpResponse(json.dumps(ret))