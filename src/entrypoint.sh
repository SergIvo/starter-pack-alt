#!/bin/sh
python manage.py migrate
python manage.py createsuperuser --no-input
gunicorn project.wsgi:application --access-logfile -
