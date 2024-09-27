# Generated by Django 5.0 on 2024-09-10 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_school_students_index_no_alter_assessment_date_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='staffs_id',
            new_name='staff_id',
        ),
        migrations.AlterField(
            model_name='assessment',
            name='date_time',
            field=models.DateField(default=datetime.datetime(2024, 9, 10, 16, 2, 24, 46764, tzinfo=datetime.timezone.utc), max_length=20, verbose_name='Date Created'),
        ),
    ]
