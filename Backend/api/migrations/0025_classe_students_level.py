# Generated by Django 5.0 on 2024-09-08 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_academicyear_period_division_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='students_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.educationallevel', verbose_name='Students Level'),
        ),
    ]
