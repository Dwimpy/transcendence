# Generated by Django 4.2.7 on 2024-01-19 10:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0005_alter_ponglobby_lobby_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponglobby',
            name='lobby_id',
            field=models.UUIDField(default=uuid.UUID('8121aead-15c2-4ef2-a5b9-0d78986d4455'), editable=False, unique=True, verbose_name=uuid.uuid4),
        ),
    ]
