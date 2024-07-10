#!/bin/sh

# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

export DJANGO_SETTINGS_MODULE=transcendence.settings

# Flush the database (use with caution, this will delete all data)
# python manage.py flush --no-input

# Create and apply migrations for each app
for app in $(ls -d */ | cut -f1 -d'/'); do
  python manage.py makemigrations $app
  python manage.py migrate $app
done

# Apply any remaining migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run the server
daphne -e ssl:443:privateKey=/certs/django.key:certKey=/certs/django.crt transcendence.asgi:application
