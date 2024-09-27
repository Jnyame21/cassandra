# Generated by Django 5.0 on 2024-09-12 06:16

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_alter_studentattendance_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectassignment',
            name='hod',
        ),
        migrations.AddField(
            model_name='subjectassignment',
            name='assigned_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_by', to='api.staff', verbose_name='Assigned By'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='date_time',
            field=models.DateField(default=datetime.datetime(2024, 9, 12, 6, 16, 25, 212072, tzinfo=datetime.timezone.utc), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='department',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='head',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='program',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='school',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='date',
            field=models.DateField(default=datetime.date(2024, 9, 12), verbose_name='Attendance Date'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='subjectassignment',
            name='date_created',
            field=models.DateField(default=datetime.date(2024, 9, 12), max_length=20, verbose_name='Date Created'),
        ),
    ]
