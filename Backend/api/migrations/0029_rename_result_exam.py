# Generated by Django 5.0 on 2024-09-09 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_gradingsystem_remark_alter_gradingsystem_label_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Result',
            new_name='Exam',
        ),
    ]