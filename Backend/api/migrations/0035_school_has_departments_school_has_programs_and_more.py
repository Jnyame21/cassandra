# Generated by Django 5.0 on 2024-09-10 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_assessment_comment_assessment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='has_departments',
            field=models.BooleanField(default=True, verbose_name='Does the school has departments?'),
        ),
        migrations.AddField(
            model_name='school',
            name='has_programs',
            field=models.BooleanField(default=True, verbose_name='Does the school has programs?'),
        ),
        migrations.AddField(
            model_name='school',
            name='students_id',
            field=models.BooleanField(default=False, verbose_name='Does the school give student ID numbers?'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='date_time',
            field=models.DateField(default=datetime.datetime(2024, 9, 10, 14, 53, 32, 888346, tzinfo=datetime.timezone.utc), max_length=20, verbose_name='Date Created'),
        ),
    ]
