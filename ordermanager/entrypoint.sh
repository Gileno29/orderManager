#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python create_user.py
gunicorn --timeout 60 --workers 3 ordermanager.wsgi:application --bind 0.0.0.0:8000      