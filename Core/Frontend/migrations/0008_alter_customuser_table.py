# Generated by Django 4.2.7 on 2024-01-09 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0007_alter_customuser_options_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]
