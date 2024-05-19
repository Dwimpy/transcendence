from django.conf import settings
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
import pyotp
from twilio.rest import Client

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    devices = models.ManyToManyField(TOTPDevice)
    chosen_2fa_method = models.CharField(
        max_length=50, 
        choices=[('qr', 'QR Code'), ('sms', 'SMS'), ('email', 'Email')], 
        default='qr',
        blank=True,
        null=True
    )

class TwilioSMSDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    key = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)

    def generate_token(self):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        token = pyotp.TOTP(self.key).now()
        message = client.messages.create(
            body=f'Your authentication token is {token}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=self.phone_number
        )
        return token

class EmailOTPDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)