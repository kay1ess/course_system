from django.contrib import admin
from teacher import models
# Register your models here.
admin.site.register(models.Weeks)
admin.site.register(models.Times)
admin.site.register(models.Classroom)
admin.site.register(models.Teacher)