# Generated by Django 5.0 on 2024-09-09 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_academicyear_date_created_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gradingsystem',
            unique_together={('label', 'school')},
        ),
    ]
