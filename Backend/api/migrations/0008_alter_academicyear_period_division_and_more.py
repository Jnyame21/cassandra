# Generated by Django 5.0 on 2024-10-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_staff_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='period_division',
            field=models.CharField(default='SEMESTER', max_length=20, verbose_name='Period Division Name'),
        ),
        migrations.AddField(
            model_name='academicyear',
            name='number_of_divisions',
            field=models.IntegerField(default=2, verbose_name='Number of Divisions'),
        ),
        migrations.AddField(
            model_name='educationallevel',
            name='years_to_complete',
            field=models.IntegerField(default=3, verbose_name='Years to Complete'),
        ),
        migrations.AlterUniqueTogether(
            name='educationallevel',
            unique_together={('name', 'years_to_complete')},
        ),
        migrations.DeleteModel(
            name='AcademicYearDivision',
        ),
    ]
