# Generated by Django 5.0 on 2024-04-20 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_alter_studentattendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='date',
            field=models.DateField(default=datetime.date(2024, 4, 20), verbose_name='Attendance Date'),
        ),
    ]
