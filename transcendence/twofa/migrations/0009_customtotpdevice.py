# Generated by Django 4.2.7 on 2024-05-27 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otp_totp', '0003_add_timestamps'),
        ('twofa', '0008_alter_emailotpdevice_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTOTPDevice',
            fields=[
            ],
            options={
                'verbose_name': 'QR Code Device',
                'verbose_name_plural': 'QR Code Devices',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('otp_totp.totpdevice',),
        ),
    ]