@echo off
python manage.py migrate
python manage.py makemigrations
start cmd.exe /C "python login.py runserver" 
python manage.py runserver
pause
