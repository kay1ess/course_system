import json

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from edu.form import PubForm, NewsForm, SearchForm, NewsSearchForm, TeacherSearchForm, AddTeacher
from edu.models import NewCourse, News, EduAdmin
from student.models import StuSelected
from teacher.models import AppliedCourse, Teacher
from course.ulti import MyPagination

# Create your views here.

def check_group3(user):
    g_name = user.groups.all().first()
    g_id = Group.objects.filter(name=g_name).first().id
    return (True if g_id==3 else False)


@login_required
@user_passes_test(check_group3)
def index(request):
    app_list = AppliedCourse.objects.filter(status='None')
    apps = app_list.count()
    return render(request, "edu_index.html", locals())

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
        if obj.is_valid():
            try:
                News.objects.create(
                    title=obj.cleaned_data.get("title"),
                    content=obj.cleaned_data.get("content"),
                    watchers=obj.cleaned_data.get("watchers"),
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
        no = request.GET.get('clsNo')
        AppliedCourse.objects.filter(np=no).update(status=True)
        c = AppliedCourse.objects.filter(no=no).first()
        StuSelected.objects.create(
            no=c.no,
            name=c.name,
            college_id=c.college.id,
            time_id=c.time.id,
            week_id=c.week.id,
            select_course_id=c.id,
            teacher_id=c.teacher.id,
            credit=c.credit,
            classroom_id=c.classroom.id
        )
        NewCourse.objects.filter(no=no).update(status=2)

    except Exception as e:
        print(str(e))
        ret["status"] = False
        ret["msg"] = "数据库操作失败，请联系系统管理员"
    return HttpResponse(json.dumps(ret))

@login_required
@user_passes_test(check_group3)
def nopass_(request):
    ret = {"status":True,"msg":"该课程审批被拒绝！"}
    try:
        no = request.GET.get('clsNo')
        AppliedCourse.objects.filter(no=no).update(status=False)
        NewCourse.objects.filter(no=no).update(status=3)
    except Exception as e:
        print(str(e))
        ret["status"] = False
        ret["msg"] = "数据库操作失败，请联系系统管理员"
    return HttpResponse(json.dumps(ret))

@login_required
@user_passes_test(check_group3)
def manager_center(request):
    if request.method == "GET":
        obj = AddTeacher()
        return render(request, "manage_center.html", locals())
    if request.method == "POST":
        ret = {"status":True,"msg":None}
        obj = AddTeacher(request.POST)
        if obj.is_valid():
            try:
                no = obj.cleaned_data.get("no")
                name = obj.cleaned_data.get("name")
                gender = obj.cleaned_data.get("gender")
                card_id = obj.cleaned_data.get("card_id")
                college_id = obj.cleaned_data.get("college_id")
                position_id = obj.cleaned_data.get("position_id")
                email = obj.cleaned_data.get("email")
                tel = obj.cleaned_data.get("tel")



                User.objects.create(username=no,password=card_id[12:18])
                user =  User.objects.filter(username=no).first()
                no_id = user.id
                if gender == 2:
                    gender = 0
                Teacher.objects.create(
                    no_id=no_id,
                    name=name,
                    gender=gender,
                    card_id=card_id,
                    college_id=college_id,
                    position_id=position_id,
                    email=email,
                    tel=tel,
                    birth=card_id[6:12]
                )
                user.groups.add(2)

                ret["msg"] = "创建成功"

            except Exception as e:
                ret["status"] = False
                if str(e) == "UNIQUE constraint failed: teacher_teacher.no":
                    ret["msg"] = "课程号已经被使用，请重写填写"
                else:
                    ret["msg"] = "数据库写入异常，请联系管理员，错误代码:"+str(e)
            return HttpResponse(json.dumps(ret))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            return  HttpResponse(json.dumps(ret))



@login_required
@user_passes_test(check_group3)
def m_course(request):
    if request.method == "GET":
        fm = SearchForm()
        c = NewCourse.objects.all()
        cours = c.order_by("ctime")
        cours_r = c.order_by("-ctime")
        no = c.order_by("no")
        no_r = c.order_by("-no")
        obj = MyPagination(cours_r.count(), request.GET.get("p"), 10, url='m_course')
        data = cours[obj.start():obj.end()]
        return render(request, "m_course.html", locals())
    if request.method == "POST":
        fm = SearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                cours_r = NewCourse.objects.filter(no__contains=content).order_by("-ctime")
                obj = MyPagination(cours_r.count(), request.GET.get("p"), 10, url='m_course')
                data = cours_r[obj.start():obj.end()]
            else:
                cours_r = NewCourse.objects.filter(name__contains=content).order_by("-ctime")
                obj = MyPagination(cours_r.count(), request.GET.get("p"), 10, url='m_course')
                data = cours_r[obj.start():obj.end()]
            return render(request, 'm_course.html', {"data":data, "fm":fm})
        else:
            return HttpResponse("输入不符合要求，请重新输入")

@login_required
@user_passes_test(check_group3)
def del_course(request):
    if request.method == "POST":
        ret = {"status":True,"msg":"删除成功"}
        try:
            ls = request.POST.getlist("cno[]")
            for i in ls:
                AppliedCourse.objects.filter(no=i).delete()
                NewCourse.objects.filter(no=i).delete()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "删除失败"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def offline_course(request):
    if request.method == "POST":
        ret = {"status":True,"msg":"下线成功"}
        try:
            ls = request.POST.getlist("cno[]")
            for i in ls:
                NewCourse.objects.filter(no=i).update(status=4)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "下线失败"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def m_course_detail(request):
    cno = request.GET.get("cno")
    data = []
    course = AppliedCourse.objects.filter(no=cno)
    print(cno)
    if course:
        for cour_detail in course:
            data.extend([cour_detail.no,cour_detail.name,float(cour_detail.credit),cour_detail.college.name,
                         cour_detail.teacher.name,cour_detail.classroom.name,cour_detail.week.name,
                         cour_detail.time.duration])
    else:
        course = NewCourse.objects.filter(no=cno)
        for cour_detail in course:
            data.extend([cour_detail.no,cour_detail.name,float(cour_detail.credit),cour_detail.college.name])
    return HttpResponse(json.dumps(data, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def online_course(request):
    if request.method == "POST":
        ret = {"status":True}
        cno = request.POST.get("cno")
        try:
            NewCourse.objects.filter(no=cno).update(status=0)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception:
            ret["status"] = False
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def m_news(request):
    if request.method == "GET":
        fm = NewsSearchForm()
        n = News.objects.all()
        news = n.order_by("m_time")
        news_r = n.order_by("-m_time")
        obj = MyPagination(news_r.count(), request.GET.get("p"), 10, url='m_news')
        data = n[obj.start():obj.end()]
        return render(request, "m_news.html", locals())
    if request.method == "POST":
        fm = NewsSearchForm(request.POST)
        print(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            news = News.objects.filter(title__contains=content).order_by("-m_time")
            obj = MyPagination(news.count(), request.GET.get("p"), 10, url='m_news')
            data = news[obj.start():obj.end()]
            return render(request, 'm_news.html', {"data":data, "fm":fm})
        else:
            return HttpResponse("输入不符合要求，请重新输入")

@login_required
@user_passes_test(check_group3)
def m_news_detail(request):
    nid = request.GET.get("nid")
    data = []
    news = News.objects.filter(id=nid)
    for n in news:
        data.extend([n.title,n.content,n.c_time.strftime("%Y-%m-%d-%H-%M"),n.created_by.name,n.m_time.strftime("%Y-%m-%d-%H-%M"),n.watchers.title()])

    return HttpResponse(json.dumps(data, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def del_news(request):
    if request.method == "POST":
        ret = {"status":True,"msg":"删除成功"}
        try:
            ls = request.POST.getlist("nid[]")
            for i in ls:
                News.objects.filter(id=i).delete()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "删除失败"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

@login_required
@user_passes_test(check_group3)
def mod_news(request, nid):
    if request.method == "GET":
        news = News.objects.get(id=nid)
        obj = NewsForm({
            'title':news.title,
            'content':news.content,
            'watchers':news.watchers
        })
        return render(request,"mod_news.html", locals())
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        obj = NewsForm(request.POST)
        if obj.is_valid():

            News.objects.filter(id=nid).update(
                title=obj.cleaned_data.get("title"),
                content = obj.cleaned_data.get("content"),
                watchers = obj.cleaned_data.get("watchers")
            )
            try:
                ret["msg"] = "修改成功"
            except Exception as e:
                print(e)
                ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:

            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


def m_student(request):
    pass

def m_teacher(request):
    if request.method == "GET":
        fm = TeacherSearchForm()
        t = Teacher.objects.all()
        obj = MyPagination(t.count(), request.GET.get("p"), 10, url='m_teacher')
        teachers = t[obj.start():obj.end()]
        return render(request, "m_teacher.html", {"teachers":teachers,"obj":obj,"fm":fm})
    if request.method == "POST":
        fm = TeacherSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                t = Teacher.objects.filter(no__username__contains=content)
                obj = MyPagination(t.count(), request.GET.get("p"), 10, url='m_teacher')
                teachers = t[obj.start():obj.end()]

            else:
                t = Teacher.objects.filter(name__contains=content)
                obj = MyPagination(t.count(), request.GET.get("p"), 10, url='m_teacher')
                teachers = t[obj.start():obj.end()]
            return render(request, 'm_teacher.html', {"teachers":teachers, "fm":fm})
        else:
            return HttpResponse("输入不符合要求，请重新输入")
def del_teacher(request):
    if request.method == "POST":
        ret = {"status":True,"msg":"删除成功"}
        try:
            ls = request.POST.getlist("tno[]")
            for i in ls:
                User.objects.filter(username=i).delete()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "删除失败"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

def teacher_detail(request):
    tno = request.GET.get("tno")
    data = []
    teachers = Teacher.objects.filter(no__username=tno)

    for teacher in teachers:
        if teacher.gender:
            teacher.gender = "男"
        else:
            teacher.gender = "女"
        data.extend([teacher.name,teacher.no.username,teacher.gender,teacher.college.name,
                     teacher.position.name,
                     teacher.email,
                     teacher.tel,teacher.birth
                     ])
    return HttpResponse(json.dumps(data, ensure_ascii=False))

def resetPwd(request):
    if request.method == "POST":
        ret = {"status":True, "msg":None}
        no = request.POST.get("no")
        try:
            card_id = Teacher.objects.get(no__username=no).card_id
            user = User.objects.get(username=no)
            user.set_password(raw_password=card_id[12:18])
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        except Exception as e:
            print(str(e))
            ret["status"] = False
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

