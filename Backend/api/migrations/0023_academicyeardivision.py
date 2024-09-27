# Generated by Django 5.0 on 2024-09-08 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_head_level_staff_level_student_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYearDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Academic Year Division Name')),
            ],
        ),
    ]