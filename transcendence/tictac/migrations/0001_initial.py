# Generated by Django 4.2.7 on 2024-05-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.CharField(default='         ', max_length=9)),
                ('current_turn', models.CharField(default='X', max_length=1)),
                ('is_over', models.BooleanField(default=False)),
                ('winner', models.CharField(blank=True, max_length=1, null=True)),
            ],
        ),
    ]
