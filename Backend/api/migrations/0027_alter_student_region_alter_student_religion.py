# Generated by Django 5.0 on 2024-11-06 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_remove_staff_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='region',
            field=models.CharField(default='', max_length=100, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(default='', max_length=100, verbose_name='Religion'),
        ),
    ]
