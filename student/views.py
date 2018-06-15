import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from edu.models import News
from teacher.models import AppliedCourse, Weeks
from student.models import PwdStatus, FinalSelect
from teacher.models import Times
from student.models import StuSelected
from student.models import Student
from edu.form import LoginForm
from edu.form import ChangePwdForm

# Create your views here.
def check_group1(user):
    g_name = user.groups.all().first()
    g_id = Group.objects.filter(name=g_name).first().id
    return (True if g_id==1 else False)

@login_required
@user_passes_test(check_group1)
def index(request):
    s_id = Student.objects.filter(no__username=request.user).first().id
    today_ = datetime.datetime.now().weekday() + 1
    today_courses = FinalSelect.objects.filter(student_id=s_id, week_id=today_)
    news = News.objects.filter(Q(watchers='1') | Q(watchers='3')).order_by("-m_time", "-c_time")[:5]
    return render(request, "s_index.html", locals())

@login_required
@user_passes_test(check_group1)
def select(request):
    s_id = Student.objects.filter(no__username=request.user).first().id
    courses = StuSelected.objects.filter(~Q(student_id=s_id))
    return render(request, "s_select.html", {"courses":courses})

@login_required
@user_passes_test(check_group1)
def selected(request):
    id = Student.objects.filter(no__username=request.user).first().id
    courses = FinalSelect.objects.filter(student_id=id)
    return render(request, "s_selected.html", {"courses":courses})


@login_required
@user_passes_test(check_group1)
def courses(request):
    id = Student.objects.filter(no__username=request.user).first().id
    cour = FinalSelect.objects.filter(student_id=id)
    times = Times.objects.all()
    weeks = Weeks.objects.all()
    return render(request, "s_courses.html", {"times":times, "weeks":weeks, "cour":cour})

@login_required
@user_passes_test(check_group1)
def info(request):
    pass

@login_required
@user_passes_test(check_group1)
def choosed(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "选课成功！"}
        s_id = Student.objects.filter(no__username=request.user).first().id
        try:

            StuSelected.objects.filter(no=request.POST.get("no")).update(
                student_id=s_id
            )
            FinalSelect.objects.create(
                no=request.POST.get("no"),
                name=request.POST.get("name"),
                college_id=request.POST.get("college"),
                time_id=request.POST.get("time"),
                week_id=request.POST.get("week"),
                select_course_id=request.POST.get("cid"),
                teacher_id=request.POST.get("teacher"),
                credit=request.POST.get("credit"),
                classroom_id=request.POST.get("classroom"),
                student_id=s_id
            )
            AppliedCourse.objects.filter(no=request.POST.get("no")).update(choose=True)

        except Exception as e:
            if str(e) == "UNIQUE constraint failed: student_finalselect.week_id, student_finalselect.student_id, student_finalselect.time_id":
                StuSelected.objects.filter(no=request.POST.get("no")).update(
                    student_id=None
                )
                AppliedCourse.objects.filter(no=request.POST.get("no")).update(choose=None)
                ret["status"] = False
                ret["msg"] = "该时间段发生冲突，请在空余的时间进行选择"
                return HttpResponse(json.dumps(ret))
            print(str(e))
            StuSelected.objects.filter(no=request.POST.get("no")).update(
                student_id=None
            )
            AppliedCourse.objects.filter(no=request.POST.get("no")).update(choose=None)
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



                    login(request, user)



                    # if u is False:
                    #     if user.last_login is None:
                    #         ret["msg"] = 0
                    #         return HttpResponse(json.dumps(ret, ensure_ascii=False))

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
@login_required
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
                if password1 == old_password:
                    ret["status"] = "not_ok"
                    ret["msg"] = "新密码不与旧密码相同"
                else:
                    if password1 == password2:
                        ret["status"] = "success"
                        # 这种改法 直接明文写入数据库 不对 也不好
                        # User.objects.filter(username=request.user).update(password=password1)
                        user.set_password(password1)
                        user.save()
                        PwdStatus.objects.filter(user__username=user).update(pwd_status=True)

                        return HttpResponse(json.dumps(ret, ensure_ascii=False))
                    else:
                        ret["status"] = "diff_failed"
                        ret["msg"] = "两次密码输入不一致，请重新输入"
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = "form_failed"
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
