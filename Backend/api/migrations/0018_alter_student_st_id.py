# Generated by Django 5.0 on 2024-09-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_department_date_created_head_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='st_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Student ID.'),
        ),
    ]
