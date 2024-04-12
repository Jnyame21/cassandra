# Generated by Django 5.0 on 2024-01-15 15:10

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_alter_classe_created_at_alter_head_date_enrolled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classe',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 15), verbose_name='Attendance Date'),
        ),
    ]