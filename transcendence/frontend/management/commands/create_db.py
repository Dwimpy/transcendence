# yourapp/management/commands/create_db.py

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create the PostgreSQL database if it does not exist.'

    def handle(self, *args, **options):
        database_name = connection.settings_dict['NAME']

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
            database_exists = cursor.fetchone()

        if not database_exists:
            self.stdout.write(self.style.SUCCESS(f"Database '{database_name}' does not exist. Creating..."))
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {database_name}")

            self.stdout.write(self.style.SUCCESS("Database created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Database '{database_name}' already exists."))
