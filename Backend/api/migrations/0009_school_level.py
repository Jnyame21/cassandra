# Generated by Django 5.0 on 2024-10-25 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_academicyear_period_division_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.educationallevel', verbose_name='Educational Level'),
        ),
    ]
