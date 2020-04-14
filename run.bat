@echo off
python log_in.py
cls
python manage.py migrate
python manage.py makemigrations
cls
explorer "http://127.0.0.1:8000/"
python manage.py runserver

pause
