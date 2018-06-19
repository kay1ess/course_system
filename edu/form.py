from django import forms
from django.core.validators import RegexValidator
from django.forms import fields, widgets
from edu.models import College, News, Position, Grade


class PubForm(forms.Form):
    no = fields.CharField(
        required=True,
        label="课程号",
        validators=[RegexValidator(r'\d{8}', "请输入数字")],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '课程号为8位数字'
        }
        )
    name = fields.CharField(
        max_length=30,
        min_length=2,
        required=True,
        label="课程名",
        error_messages={
            'max_length': '最大不能超过30个字',
            'min_length': '最小不能少于2个字',
            'invalid': '不符合格式要求'
        }
    )

    credit = fields.DecimalField(max_digits=2, decimal_places=1, max_value=5.0,
                                 error_messages={
                                     'invalid':'必须为一位小数',
                                     'max_value': '最大学分不应该超过5.0'
                                 },
                                 label="学分"

                                 )
    college_id = fields.IntegerField(widget=widgets.Select(),label="授课学院")
    def __init__(self, *args, **kwargs):
        super(PubForm, self).__init__(*args, **kwargs)
        self.fields['college_id'].widget.choices = College.objects.values_list("id", "name")


class NewsForm(forms.ModelForm):
    title = fields.CharField(
            widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"在此输入标题"})
            )
    choices = ((1, 'Everyone'),
               (2, 'Teachers'),
               (3, 'Students'),)
    watchers = fields.CharField(
            widget=widgets.Select(choices=choices),
            label="可见对象",

    )
    class Meta:
        model = News
        fields = ["title","content","watchers"]



class LoginForm(forms.Form):
    username = fields.CharField(
            widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"学号/工号"}),
            label="ID",
            validators=[RegexValidator(r'\d{8,13}')],
            error_messages={
                'required': '该字段必须要输入',
                'invalid':'输入不符合要求'
            }
    )

    password = fields.CharField(
        widget=widgets.TextInput(attrs={"type":"password","class": "form-control", "placeholder": "在这里输入密码"}),
        label="密码",
        help_text="初始密码为身份证后6位"
    )
    choices = (
        (1, "学生"),
        (2, "教师"),
        (3, "教务"),
    )
    group_id = fields.IntegerField(widget=widgets.RadioSelect(choices=choices), label="选择你的身份")


class ChangePwdForm(forms.Form):
    old_password = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "在这里输入旧密码"}),
        label="旧密码",
        help_text="初始密码为身份证后6位"
    )

    password1 = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "在这里输入新密码"}),
        validators=[RegexValidator(r'\w{8,18}')],
        label="新密码",
        help_text="密码应含有字母或数字，且长度为8-18个字符",
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入密码不符合要求'
        }

    )

    password2 = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "再次输入新密码"}),
        label="确认新密码",
        help_text="密码应含有字母或数字，且长度不小于8个字符",
        validators = [RegexValidator(r'\w{8,18}')],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入密码不符合要求'
        }
    )

class SearchForm(forms.Form):
    content = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"请输入课程号或课程名"}),
        max_length=30
    )

class NewsSearchForm(forms.Form):
    content = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"请输入新闻标题"}),
        max_length=30
    )


class TeacherSearchForm(forms.Form):
    content = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入姓名或工号"}),
    )

class StudentSearchForm(forms.Form):
    content = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入姓名或学号"}),
    )

class AddTeacher(forms.Form):
    no = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control ","placeholder":"请输入工号"}),
        validators=[RegexValidator(r'\d{8}')]
    )
    name = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入姓名"}),
    )
    choices = (
        (1,'男'),
        (2,'女'),
    )
    gender = fields.IntegerField(
        widget=widgets.Select(choices=choices),

    )
    card_id = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入身份证号"}),
        validators=[RegexValidator(r'\d{17}(\d|X)')]
    )

    position_id = fields.IntegerField(widget=widgets.Select())

    college_id = fields.IntegerField(widget=widgets.Select())

    email = fields.EmailField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入电子邮件"}),

    )

    tel = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入电话号"}),
        validators=[RegexValidator(r'\d{11}')]

    )




    def __init__(self, *args, **kwargs):
        super(AddTeacher, self).__init__(*args, **kwargs)
        self.fields['college_id'].widget.choices = College.objects.values_list("id", "name")
        self.fields['position_id'].widget.choices = Position.objects.values_list("id", "name")

class AddStudent(forms.Form):
    no = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control ","placeholder":"请输入学号"}),
        validators=[RegexValidator(r'\d{8}')]
    )
    name = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入姓名"}),
    )
    choices = (
        (1,'男'),
        (2,'女'),
    )
    gender = fields.IntegerField(
        widget=widgets.Select(choices=choices),

    )
    card_id = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入身份证号"}),
        validators=[RegexValidator(r'\d{17}(\d|X)')]
    )

    grade_id = fields.IntegerField(widget=widgets.Select())

    college_id = fields.IntegerField(widget=widgets.Select())

    email = fields.EmailField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入电子邮件"}),

    )

    tel = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入电话号"}),
        validators=[RegexValidator(r'\d{11}')]

    )




    def __init__(self, *args, **kwargs):
        super(AddStudent, self).__init__(*args, **kwargs)
        self.fields['college_id'].widget.choices = College.objects.values_list("id", "name")
        self.fields['grade_id'].widget.choices = Grade.objects.values_list("id", "name")
