# Generated by Django 5.0 on 2024-10-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_classe_academic_years_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='repeated',
            field=models.BooleanField(default=False, verbose_name='Will Repeat'),
        ),
    ]
