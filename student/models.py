from django.contrib.auth.models import User
from django.db import models
from edu.models import College
from edu.models import Grade
from teacher.models import Classroom, AppliedCourse
from teacher.models import Weeks
from teacher.models import Times
from teacher.models import Teacher

# Create your models here.


class Student(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE,db_index=True)
    name = models.CharField(max_length=20,db_index=True)
    gender = models.BooleanField()
    tel = models.CharField(max_length=11)
    card_id = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    birth = models.CharField(max_length=10)
    is_first = models.BooleanField(default=False)

class StuSelected(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time = models.ForeignKey(Times, on_delete=models.CASCADE)
    week = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    select_course = models.ForeignKey(AppliedCourse, on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.SET_NULL, null=True, default=None)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    credit = models.DecimalField(max_digits=2, decimal_places=1)



class FinalSelect(models.Model):
    no = models.CharField(max_length=8)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time = models.ForeignKey(Times, on_delete=models.CASCADE)
    week = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    select_course = models.ForeignKey(StuSelected, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    credit = models.DecimalField(max_digits=2, decimal_places=1)
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("week", "student", "time")


class PwdStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pwd_status = models.BooleanField(default=False)
    last_mtime = models.DateTimeField(auto_now=True)
