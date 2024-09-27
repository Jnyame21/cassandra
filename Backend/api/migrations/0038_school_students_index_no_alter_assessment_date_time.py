# Generated by Django 5.0 on 2024-09-10 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_remove_student_guardian_student_guardian_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='students_index_no',
            field=models.BooleanField(default=False, verbose_name='Does the school give student Index numbers?'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='date_time',
            field=models.DateField(default=datetime.datetime(2024, 9, 10, 15, 58, 43, 126371, tzinfo=datetime.timezone.utc), max_length=20, verbose_name='Date Created'),
        ),
    ]
