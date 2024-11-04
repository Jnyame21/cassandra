# Generated by Django 5.0 on 2024-10-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_exam_total_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='total_score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Total Exams Score'),
        ),
    ]