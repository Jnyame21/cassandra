# Generated by Django 5.0 on 2023-12-29 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_batch_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.CharField(default='not set', max_length=100, verbose_name='Guardian Name'),
        ),
    ]
