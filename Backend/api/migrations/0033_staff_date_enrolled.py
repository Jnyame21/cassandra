# Generated by Django 5.0 on 2024-11-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_remove_staff_date_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='date_enrolled',
            field=models.DateField(blank=True, null=True, verbose_name='Enrollment Date'),
        ),
    ]
