# Generated by Django 5.0 on 2024-09-07 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_university_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicyear',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 7), verbose_name='Date Created'),
        ),
        migrations.AddField(
            model_name='academicyear',
            name='period_division_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Academic Year Period Division Name'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='date',
            field=models.DateField(default=datetime.date(2024, 9, 7), verbose_name='Attendance Date'),
        ),
    ]
