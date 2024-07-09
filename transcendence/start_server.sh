while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
daphne -e ssl:443:privateKey=/certs/django.key:certKey=/certs/django.crt transcendence.asgi:application