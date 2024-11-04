# Generated by Django 5.0 on 2024-10-26 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_program_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='alt_contact',
            field=models.CharField(default='', max_length=15, verbose_name='Alternate Phone No'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='contact',
            field=models.CharField(default='', max_length=20, verbose_name='Phone No'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='nationality',
            field=models.CharField(default='', max_length=50, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='pob',
            field=models.CharField(default='', max_length=50, verbose_name='Home City/Town'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='region',
            field=models.CharField(default='', max_length=50, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='student',
            name='contact',
            field=models.CharField(default='', max_length=20, verbose_name='Phone No'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.CharField(default='', max_length=100, verbose_name='Guardian Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_address',
            field=models.CharField(default='', max_length=100, verbose_name='Address of guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_contact',
            field=models.CharField(default='', max_length=10, verbose_name='Phone no. of guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_email',
            field=models.CharField(default='', max_length=100, verbose_name='Guardian Email'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_gender',
            field=models.CharField(default='', max_length=100, verbose_name='Guardian Gender'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_nationality',
            field=models.CharField(default='', max_length=50, verbose_name='Nationality of Guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian_occupation',
            field=models.CharField(default='', max_length=50, verbose_name='Occupation of guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(default='', max_length=50, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='student',
            name='pob',
            field=models.CharField(default='', max_length=50, verbose_name='Home City/Town'),
        ),
        migrations.AlterField(
            model_name='student',
            name='region',
            field=models.CharField(default='', max_length=50, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(default='', max_length=50, verbose_name='Religion'),
        ),
    ]