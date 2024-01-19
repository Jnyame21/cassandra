# Generated by Django 5.0 on 2024-01-17 08:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_alter_classe_created_at_alter_studentattendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='sem_1_end_date',
            field=models.DateField(null=True, verbose_name='Term 1 End Date'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='sem_2_end_date',
            field=models.DateField(null=True, verbose_name='Term 2 End Date'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='sem_2_start_date',
            field=models.DateField(null=True, verbose_name='Term 2 Start Date'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='sem_3_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Term 3 End Date'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='sem_3_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Term 3 Start Date'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 17), verbose_name='Attendance Date'),
        ),
    ]
