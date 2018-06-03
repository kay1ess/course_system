import json

from django.http import HttpResponse
from django.shortcuts import render
from edu.form import PubForm, NewsForm
from edu.models import NewCourse, News


# Create your views here.

def index(request):
    return render(request, "edu_index.html")

def pub_course(request):
    if request.method == "GET":
        courses = NewCourse.objects.all()
        pub_form = PubForm()
        return render(request,"pubCourse.html", {"pub_form":pub_form, "courses":courses})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        pub_form = PubForm(request.POST)
        if pub_form.is_valid():
            try:

                NewCourse.objects.create(**pub_form.cleaned_data)
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

def pub_news(request):
    news_list = News.objects.all()
    return render(request, "pubNews.html", {"news_list": news_list})

def edit_news(request):
    if request.method == "GET":
        obj = NewsForm()
        return render(request, "newNews.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        obj = NewsForm(request.POST)
        print(obj)
        if obj.is_valid():
            try:
                News.objects.create(**obj.cleaned_data)
                ret["msg"] = "发布成功"
            except Exception as e:
                ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
