# Generated by Django 5.0 on 2024-10-27 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_academicyear_results_released'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='graduation_class',
        ),
        migrations.AddField(
            model_name='student',
            name='graduation_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graduation_academic_year', to='api.academicyear', verbose_name='Graduation academic year'),
        ),
    ]