from django.urls import path
from .views import setup_2fa, qr_code, verify_2fa, setup_sms_2fa, send_sms_token, setup_email_2fa, send_email_token

app_name = 'twofa'

urlpatterns = [
    path('setup/', setup_2fa, name='setup_2fa'),
    path('qr_code/', qr_code, name='qr_code'),
    path('verify/', verify_2fa, name='verify_2fa'),
    path('setup_sms/', setup_sms_2fa, name='setup_sms_2fa'),
    path('send_sms_token/', send_sms_token, name='send_sms_token'),
    path('setup_email/', setup_email_2fa, name='setup_email_2fa'),
    path('send_email_token/', send_email_token, name='send_email_token'),
]
