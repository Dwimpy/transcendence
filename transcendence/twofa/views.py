from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from .models import UserProfile, TwilioSMSDevice, EmailOTPDevice
import pyotp
from django.core.mail import send_mail
from twilio.rest import Client

@login_required
def setup_2fa(request):
    user = request.user
    # Ensure the UserProfile exists
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        method = request.POST.get('method')
        if method == 'qr':
            if not TOTPDevice.objects.filter(user=user).exists():
                secret = pyotp.random_base32()
                TOTPDevice.objects.create(user=user, name='default', key=secret)
            user_profile.chosen_2fa_method = 'qr'
        elif method == 'sms':
            return redirect('twofa:setup_sms_2fa')
        elif method == 'email':
            return redirect('twofa:setup_email_2fa')
        user_profile.save()
        return redirect('twofa:qr_code' if method == 'qr' else 'twofa:verify_2fa')
    return render(request, 'twofa/setup_2fa.html')

@login_required
def qr_code(request):
    user = request.user
    totp_device = TOTPDevice.objects.get(user=user, name='default')
    secret = totp_device.key
    totp = pyotp.TOTP(secret)
    qr_code_url = totp.provisioning_uri(user.email, issuer_name="transcendence")
    return render(request, 'twofa/enable_2fa.html', {'qr_code_url': qr_code_url})

@login_required
def verify_2fa(request):
    user = request.user
    if not request.session.get('pre_2fa_login'):
        return redirect('index')

    if request.method == 'POST':
        token = request.POST.get('otp_token')
        user_profile = UserProfile.objects.get(user=user)
        method = user_profile.chosen_2fa_method
        if method == 'qr':
            totp_device = TOTPDevice.objects.get(user=user, name='default')
            secret = totp_device.key
            totp = pyotp.TOTP(secret)
        elif method == 'sms':
            totp_device = TwilioSMSDevice.objects.get(user=user)
            secret = totp_device.key
            totp = pyotp.TOTP(secret)
        elif method == 'email':
            email_device = EmailOTPDevice.objects.get(user=user)
            secret = email_device.key
            totp = pyotp.TOTP(secret)

        if totp.verify(token):
            if method == 'qr':
                totp_device.confirmed = True
                totp_device.save()
            elif method == 'sms':
                totp_device.confirmed = True
                totp_device.save()
            elif method == 'email':
                email_device.confirmed = True
                email_device.save()
            del request.session['pre_2fa_login']
            return redirect('index')
        else:
            return render(request, 'twofa/verify_2fa.html', {'error': 'Invalid token'})
    return render(request, 'twofa/verify_2fa.html')

@login_required
def setup_sms_2fa(request):
    user = request.user
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if not TwilioSMSDevice.objects.filter(user=user).exists():
            secret = pyotp.random_base32()
            TwilioSMSDevice.objects.create(user=user, phone_number=phone_number, key=secret)
        user.userprofile.chosen_2fa_method = 'sms'
        user.userprofile.save()
        return redirect('twofa:send_sms_token')
    return render(request, 'twofa/setup_sms_2fa.html')

@login_required
def send_sms_token(request):
    user = request.user
    sms_device = TwilioSMSDevice.objects.get(user=user)
    sms_device.generate_token()
    return redirect('twofa:verify_2fa')

@login_required
def setup_email_2fa(request):
    user = request.user
    if request.method == 'POST':
        if not EmailOTPDevice.objects.filter(user=user).exists():
            secret = pyotp.random_base32()
            EmailOTPDevice.objects.create(user=user, key=secret)
        user.userprofile.chosen_2fa_method = 'email'
        user.userprofile.save()
        return redirect('twofa:send_email_token')
    return render(request, 'twofa/setup_email_2fa.html')

@login_required
def send_email_token(request):
    user = request.user
    email_device = EmailOTPDevice.objects.get(user=user)
    totp = pyotp.TOTP(email_device.key)
    token = totp.now()
    send_mail(
        'Your authentication token',
        f'Your authentication token is {token}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    return redirect('twofa:verify_2fa')
