import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from teacher.models import AppliedCourse, Weeks
from student.models import Selected
from teacher.models import Times
from student.models import StuSelected
from edu.form import LoginForm
from edu.form import ChangePwdForm

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
    times = Times.objects.all()
    cour = Selected.objects.all()
    weeks = Weeks.objects.all()
    return render(request, "s_courses.html", {"times":times, "weeks":weeks, "cour":cour})

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


def login_(request):
    if request.method == "GET":
        obj = LoginForm()
        return render(request, "login.html", {"obj":obj})
    if request.method == "POST":
        ret = {"status":None, "msg":None}
        obj = LoginForm(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            password = obj.cleaned_data.get(("password"))
            user = authenticate(request, username=username, password=password)
            g_id = obj.cleaned_data.get("group_id")

            if user:
                # 根据user到所在组
                n = user.groups.all().first()
                group = Group.objects.filter(name=n).first()

                if group.id == g_id:
                    ret["status"] = "success"

                    # 尝试从last_login作为判断 逻辑失败
                    # if user.last_login is None:
                    #     ret["msg"] = 0
                    #     return HttpResponse(json.dumps(ret, ensure_ascii=False))
                    login(request, user)

                    if group.id == 1:
                        ret["msg"] = 1
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))
                    elif group.id == 2:
                        ret["msg"] = 2
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))
                    elif group.id == 3:
                        ret["msg"] = 3
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))


                else:
                    ret["status"] = "no_success"
                    ret["msg"] = "身份选择错误，请核对后重新选择"
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))

            else:
                ret["status"] = "up_failed"
                ret["msg"]= "用户或密码错误"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = "failed"
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

def logout_(request):
    logout(request)
    return redirect("login.html")

@login_required
def change_pwd(request):
    if request.method == "GET":
        obj = ChangePwdForm()
        return render(request, "change_password.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status":None, "msg":None}
        obj = ChangePwdForm(request.POST)
        if obj.is_valid():
            old_password = obj.cleaned_data.get("old_password")
            password1 = obj.cleaned_data.get("password1")
            password2 = obj.cleaned_data.get("password2")
            user = authenticate(username=request.user, password=old_password)
            if user is None:
                ret["status"] = "old_failed"
                ret["msg"] = "旧密码输入错误，请重新输入"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))

            else:
                if password1 == password2:
                    ret["status"] = "success"
                    # 这种改法 直接明文写入数据库 不对 也不好
                    # User.objects.filter(username=request.user).update(password=password1)
                    user.set_password(password1)
                    user.save()


                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
                else:
                    ret["status"] = "diff_failed"
                    ret["msg"] = "两次密码输入不一致，请重新输入"
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = "form_failed"
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
