# Generated by Django 4.2.7 on 2024-01-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0011_alter_customuser_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
