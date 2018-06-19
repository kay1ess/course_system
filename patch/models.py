from django.db import models

class Files(models.Model):
    teacher_info_files = models.FileField(upload_to='uploads/tea/')
    student_info_files = models.FileField(upload_to='uploads/stu/')
    course_files = models.FileField(upload_to='uploads/course/')
