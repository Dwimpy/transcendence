# Generated by Django 4.2.7 on 2024-05-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twofa', '0004_alter_emailotpdevice_key_alter_twiliosmsdevice_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='chosen_2fa_method',
            field=models.CharField(blank=True, choices=[('qr', 'QR Code'), ('sms', 'SMS'), ('email', 'Email')], default='qr', max_length=50, null=True),
        ),
    ]
