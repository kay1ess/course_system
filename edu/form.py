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