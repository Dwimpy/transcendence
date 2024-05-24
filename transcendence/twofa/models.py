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
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"2fa settings for {self.user.username}"

class TwilioSMSDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    key = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    def generate_token(self):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        totp = pyotp.TOTP(self.key, interval=60)
        token = totp.now()
        client.messages.create(
            body=f'Your authentication token is {token}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=self.phone_number
        )
        return token

class EmailOTPDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    confirmed = models.BooleanField(default=False)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.username}"
