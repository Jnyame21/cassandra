# Generated by Django 5.0 on 2024-06-07 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_ugprogram_alter_knustprogram_cut_off_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='UCCProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Program Name')),
                ('degree', models.CharField(max_length=500, verbose_name='Degree')),
                ('cut_off_point_male', models.CharField(blank=True, max_length=500, null=True, verbose_name='Cut-off point for males')),
                ('cut_off_point_female', models.CharField(blank=True, max_length=500, null=True, verbose_name='Cut-off point for females')),
            ],
        ),
    ]