# Generated by Django 5.0 on 2024-10-27 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_number_of_divisions_academicyear_no_divisions'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicyear',
            name='results_released',
            field=models.IntegerField(default=0, verbose_name='Release current semester results'),
        ),
    ]