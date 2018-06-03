import json

from django.http import HttpResponse
from django.shortcuts import render
from edu.form import PubForm
from edu.models import NewCourse
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

