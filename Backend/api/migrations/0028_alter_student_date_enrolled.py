# Generated by Django 5.0 on 2024-11-07 06:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_alter_student_region_alter_student_religion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_enrolled',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Enrollment Date'),
        ),
    ]
