from django.contrib.auth.models import User
from django.db import models
from extra_app.DjangoUeditor.models import UEditorField


# Create your models here.

class Grade(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class College(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=20)
    desc = models.TextField(max_length=140)
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=10)
    level = models.CharField(max_length=4, unique=True)
    def __str__(self):
        return self.name


class EduAdmin(models.Model):
    no = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    gender = models.BooleanField()
    card_id = models.CharField(max_length=18)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    tel = models.CharField(max_length=11)
    email = models.EmailField()
    birth = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=40, null=False)
    content = UEditorField(max_length=2000,width=1000 , height=300, toolbars='normal', imagePath='news_images/',
                           filePath='news_files/', upload_settings={'imageMaxSize': 120400000},
                           settings={}, command=None, verbose_name="正文")
    c_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EduAdmin, on_delete=models.SET_NULL, null=True)
    m_time = models.DateTimeField(auto_now=True)

class NewCourse(models.Model):
    no = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=2, decimal_places=1)
    created_by = models.ForeignKey(EduAdmin, on_delete=models.SET_NULL, null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    status = models.NullBooleanField(default='None', null=True)







