
from django.contrib.auth.models import User
from django.db import models
from edu.models import Position
from edu.models import College

# Create your models here.



class Weeks(models.Model):
    name = models.CharField(max_length=7)
    def __str__(self):
        return self.name

class Times(models.Model):
    duration = models.CharField(max_length=20)
    def __str__(self):
        return self.duration

class Classroom(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class AppliedCourse(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True)
    applied_time = models.DateTimeField(auto_now_add=True)
    credit = models.DecimalField(max_digits=2, decimal_places=1)
    status = models.NullBooleanField(default='None', null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, default="1")
    time = models.ForeignKey(Times, on_delete=models.CASCADE, default="1")
    week = models.ForeignKey(Weeks, on_delete=models.CASCADE, default="1")
    choose = models.NullBooleanField(default='None', null=True)

    # 设计打败 要建立外键 来确定是否被选上 每个学生独立不受影响
    # 设计不够独立
    def __str__(self):
        self.name

class AppliedCourse_Pos_Ti(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time = models.ForeignKey(Times, on_delete=models.CASCADE)
    week = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    applied_course = models.ForeignKey(AppliedCourse, on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True)
    class Meta:
        unique_together = ("classroom", "time", "week")


class Teacher(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE,db_index=True)
    name = models.CharField(max_length=20, null=False, blank=False,db_index=True)
    gender = models.BooleanField()
    card_id = models.CharField(max_length=18)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    tel = models.CharField(max_length=11)
    birth = models.CharField(max_length=10)
    is_first = models.BooleanField(default=False)


