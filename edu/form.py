from django import forms
from django.core.validators import RegexValidator
from django.forms import fields, widgets
from edu.models import College, News



class PubForm(forms.Form):
    no = fields.CharField(
        required=True,
        label="课程号",
        validators=[RegexValidator(r'\d{8}', "请输入数字")],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入不符合格式要求'
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
    class Meta:
        model = News
        fields = ["title","content",]

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