# Generated by Django 5.0 on 2024-01-07 12:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_classe_create_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classe',
            name='create_at',
        ),
        migrations.AddField(
            model_name='classe',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 1, 7, 12, 35, 7, 968902, tzinfo=datetime.timezone.utc), verbose_name='Created At'),
        ),
    ]
