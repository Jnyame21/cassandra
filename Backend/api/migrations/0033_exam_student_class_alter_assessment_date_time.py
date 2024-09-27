# Generated by Django 5.0 on 2024-09-09 21:50

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_assessment_student_class_alter_assessment_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='student_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.classe', verbose_name='Student Class'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='date_time',
            field=models.DateField(default=datetime.datetime(2024, 9, 9, 21, 50, 24, 58458, tzinfo=datetime.timezone.utc), max_length=20, verbose_name='Date Created'),
        ),
    ]