"""course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from edu import views as e_views
from extra_app.DjangoUeditor import urls as DjangoUeditor_urls
from teacher import views as t_views
from student import views as s_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ueditor/', include(DjangoUeditor_urls)),

    path('e/index.html', e_views.index),
    path('e/pubCourse.html', e_views.pub_course),
    path('e/pubNews.html', e_views.pub_news),
    path('e/newNews.html', e_views.edit_news),
    path('e/approve.html', e_views.approve),
    path('e/manageCenter.html', e_views.manager_center),

    path('m_course',e_views.m_course),

    path('del_course', e_views.del_course),
    path('offline_course', e_views.offline_course),
    path('m_course_detail',e_views.m_course_detail),
    path('online_course', e_views.online_course),

    path('m_news',e_views.m_news),
    path('m_news_detail', e_views.m_news_detail),
    path('del_news', e_views.del_news),
    re_path(r'mod_news.html(?P<nid>\d+)', e_views.mod_news, name="mod_news"),


    path('m_teacher',e_views.m_teacher),
    path('del_teacher',e_views.del_teacher),
    path('teacher_detail',e_views.teacher_detail),
    path('editTeacher',e_views.editTeacher),

    path('m_student', e_views.m_student),
    path('del_student',e_views.del_student),
    path('student_detail',e_views.student_detail),
    path('editStudent',e_views.editStudent),
    path('addStudent', e_views.addStudent),



    path(r'e/Pass', e_views.pass_),
    path(r'e/noPass', e_views.nopass_),

    path('t/index.html', t_views.index),
    path('t/appCourse.html', t_views.app_course),
    path('t/appliedCourse.html', t_views.applied_course),
    path('t/teachPlan.html', t_views.teach_plan),
    path('t/info.html', t_views.info),

    path('s/index.html', s_views.index),
    path('s/select.html', s_views.select),
    path('s/selected.html', s_views.selected),
    path('s/courses.html', s_views.courses),

    path('s/choosed', s_views.choosed),

    path('login.html', s_views.login_),
    path("logout.html", s_views.logout_, name="logout_"),

    path("change_password.html", s_views.change_pwd, name="change_pwd"),

    path("resetPwdTea",e_views.resetPwdTea),
    path("resetPwdStu",e_views.resetPwdStu)
]
