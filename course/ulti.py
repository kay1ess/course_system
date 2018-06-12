from django.shortcuts import render_to_response
from student.models import Student
from teacher.models import Teacher
from edu.models import EduAdmin

def my_render(request, template, context={}):
    context['user'] = request.user

    return render_to_response(template, context)

def username(request):

    return {'s_username':Student.objects.filter(no__username=request.user).first(),
            't_username':Teacher.objects.filter(no__username=request.user).first(),
            'e_username':EduAdmin.objects.filter(no__username=request.user).first(),
            }

