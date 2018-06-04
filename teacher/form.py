from django import forms
from django.forms import fields, widgets
from teacher.models import Classroom
from teacher.models import Times
from teacher.models import Weeks
from django.forms.models import ModelChoiceField

class AppForm(forms.Form):
    no = fields.CharField()
    name = fields.CharField()
    college_id = fields.CharField()
    credit = fields.CharField()
    classroom_id = fields.IntegerField(widget=widgets.Select())
    week_id = fields.IntegerField(widget=widgets.Select())
    time_id = fields.IntegerField(widget=widgets.Select())

    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        self.fields['classroom_id'].widget.choices = Classroom.objects.values_list("id","name")
        self.fields['week_id'].widget.choices = Weeks.objects.values_list("id","name")
        self.fields['time_id'].widget.choices = Times.objects.values_list("id","duration")