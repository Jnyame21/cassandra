# Generated by Django 5.0 on 2024-10-27 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_graduatedclasse'),
    ]

    operations = [
        migrations.AddField(
            model_name='graduatedclasse',
            name='graduated_class_name',
            field=models.CharField(default='', max_length=50, verbose_name='Name of the classs students graduated from'),
        ),
        migrations.AddField(
            model_name='graduatedclasse',
            name='graduation_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.academicyear', verbose_name='Graduation academic year'),
        ),
    ]
