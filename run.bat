@echo off
python manage.py migrate
python manage.py makemigrations
python log_in.py
cls
explorer "http://127.0.0.1:8000/"
python manage.py runserver

pause

