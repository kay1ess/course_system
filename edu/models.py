from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Grade(models.Model):
    name = models.CharField(max_length=10)

class College(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=20)
    desc = models.TextField(max_length=140)

class Position(models.Model):
    name = models.CharField(max_length=10)
    level = models.CharField(max_length=4, unique=True)



class EduAdmin(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    gender = models.BooleanField()
    card_id = models.CharField(max_length=18)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    tel = models.CharField(max_length=11)
    email = models.EmailField()
    birth = models.CharField(max_length=10)

class News(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=2000)
    c_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EduAdmin, on_delete=models.SET_NULL, null=True)

class NewCourse(models.Model):
    no = models.CharField(max_length=8)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=2, decimal_places=1)
    created_by = models.ForeignKey(EduAdmin, on_delete=models.SET_NULL, null=True)
    status = models.NullBooleanField(default='null', null=True)







