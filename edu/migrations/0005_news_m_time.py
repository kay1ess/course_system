# Generated by Django 2.0.4 on 2018-06-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0004_auto_20180603_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='m_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
