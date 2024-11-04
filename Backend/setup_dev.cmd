@echo off
set DJANGO_SETTINGS_MODULE=Backend.development
a_cassandra
python manage.py runserver