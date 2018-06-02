from django.contrib.auth.models import User
from django.db import models
from edu.models import Position
from edu.models import College

# Create your models here.

class Weeks(models.Model):
    name = models.CharField(max_length=7)

class Times(models.Model):
    duration = models.CharField(max_length=20)

class Classroom(models.Model):
    name = models.CharField(max_length=20)


class AppliedCourse(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True)
    applied_time = models.DateTimeField(auto_now_add=True)
    credit = models.DecimalField(max_digits=2, decimal_places=1)
    status = models.NullBooleanField(default='null', null=True, blank=True)

class AppliedCourse_Pos_Ti(models.Model):
    id = models.AutoField(primary_key=True)
    a_classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    a_time = models.ForeignKey(Times, on_delete=models.CASCADE)
    a_week = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    applied_course = models.ForeignKey(AppliedCourse, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("a_classroom", "a_time", "a_week", "applied_course")


class Teacher(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    gender = models.BooleanField()
    card_id = models.CharField(max_length=18)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    tel = models.CharField(max_length=11)
    birth = models.CharField(max_length=10)


