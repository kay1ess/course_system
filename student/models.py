from django.contrib.auth.models import User
from django.db import models
from edu.models import College
from edu.models import Grade
from teacher.models import Classroom
from teacher.models import Weeks
from teacher.models import Times
from teacher.models import Teacher

# Create your models here.

class CoursePool(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    a_week = models.ForeignKey(Weeks, on_delete=models.SET_NULL, null=True)
    a_time = models.ForeignKey(Times, on_delete=models.SET_NULL, null=True)
    credit = models.DecimalField(max_digits=2, decimal_places=1)


class Student(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    gender = models.BooleanField()
    tel = models.CharField(max_length=11)
    card_id = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    birth = models.CharField(max_length=10)
    selected_course = models.ManyToManyField(CoursePool)
