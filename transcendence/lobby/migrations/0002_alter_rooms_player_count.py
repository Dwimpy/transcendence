# Generated by Django 4.2.7 on 2024-02-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='player_count',
            field=models.IntegerField(default=0),
        ),
    ]
