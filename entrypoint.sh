#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=config.settings.development \

echo 'Applying migrations...'
python manage.py wait_for_db --settings=config.settings.development \
python manage.py makemigrations --settings=config.settings.development \
python manage.py migrate --settings=config.settings.development \

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.development config.wsgi:application --bind 0.0.0.0:8000