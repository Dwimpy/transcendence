#!/bin/bash

# while ! nc -z db 5432; do
#   echo "Waiting for PostgreSQL to be ready..."
#   sleep 1
# done
export DJANGO_SETTINGS_MODULE=transcendence.settings

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

daphne -e ssl:443:privateKey=~/certs/django.key:certKey=~/certs/django.crt transcendence.asgi:application


#daphne -e ssl:443:privateKey=/Users/kmorunov/certs/django.key:certKey=/Users/kmorunov/certs/django.crt transcendence.asgi:application
