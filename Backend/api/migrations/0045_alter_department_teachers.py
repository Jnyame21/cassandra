# Generated by Django 5.0 on 2024-01-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_alter_department_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='department_teachers', to='api.staff', verbose_name='Teachers'),
        ),
    ]