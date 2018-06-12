import json

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from edu.form import PubForm, NewsForm
from edu.models import NewCourse, News, EduAdmin
from teacher.models import AppliedCourse

# Create your views here.

def check_group3(user):
    g_name = user.groups.all().first()
    g_id = Group.objects.filter(name=g_name).first().id
    return (True if g_id==3 else False)


@login_required
@user_passes_test(check_group3)
def index(request):
    return render(request, "edu_index.html")

@login_required
@user_passes_test(check_group3)
def pub_course(request):
    if request.method == "GET":
        courses = NewCourse.objects.all().order_by('-ctime')
        pub_form = PubForm()
        return render(request,"pubCourse.html", {"pub_form":pub_form, "courses":courses})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        pub_form = PubForm(request.POST)
        if pub_form.is_valid():
            try:

                NewCourse.objects.create(**pub_form.cleaned_data,created_by_id=EduAdmin.objects.filter(no__username=request.user).first().id)
                ret["msg"] = "发布成功"

            except Exception as e:
                ret["status"] = False
                if str(e) == "UNIQUE constraint failed: edu_newcourse.no":
                    ret["msg"] = "课程号已经被使用，请重写填写"
                else:
                    ret["msg"] = "数据库写入异常，请联系管理员，错误代码:"+str(e)
            return HttpResponse(json.dumps(ret))
        else:
            ret["status"] = False
            ret["msg"] = pub_form.errors
            return  HttpResponse(json.dumps(ret))

@login_required
@user_passes_test(check_group3)
def pub_news(request):
    news_list = News.objects.all().order_by("-c_time")
    return render(request, "pubNews.html", {"news_list": news_list})

@login_required
@user_passes_test(check_group3)
def edit_news(request):
    if request.method == "GET":
        obj = NewsForm()
        return render(request, "newNews.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        obj = NewsForm(request.POST)
        print(EduAdmin.objects.filter(no__username=request.user))

        if obj.is_valid():
            try:
                News.objects.create(
                    title=obj.cleaned_data.get("title"),
                    content=obj.cleaned_data.get("content"),
                    created_by_id=EduAdmin.objects.filter(no__username=request.user).first().id
                )

                ret["msg"] = "发布成功"
            except Exception as e:
                print(e)
                ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def approve(request):
    app_list = AppliedCourse.objects.filter(status='None')
    return render(request, "e_approve.html", {"app_list":app_list})

@login_required
@user_passes_test(check_group3)
def pass_(request):
    ret = {"status":True,"msg":"该课程审批通过！"}
    try:
        id = request.GET.get('appId')
        AppliedCourse.objects.filter(id=id).update(status=True)
        NewCourse.objects.filter(id=id).update(status=False)

    except Exception:
        ret["status"] = False
        ret["msg"] = "数据库操作失败，请联系系统管理员"
    return HttpResponse(json.dumps(ret))

@login_required
@user_passes_test(check_group3)
def nopass_(request):
    ret = {"status":True,"msg":"该课程审批被拒绝！"}
    try:
        id = request.GET.get('appId')
        AppliedCourse.objects.filter(id=id).update(status=False)
    except Exception:
        ret["status"] = False
        ret["msg"] = "数据库操作失败，请联系系统管理员"
    return HttpResponse(json.dumps(ret))