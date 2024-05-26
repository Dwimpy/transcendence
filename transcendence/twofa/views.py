from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Add this import
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import UserProfile, TwilioSMSDevice, EmailOTPDevice
import pyotp
from django.core.mail import send_mail
import logging
import urllib.parse

logger = logging.getLogger(__name__)

@login_required
def setup_2fa(request):
    user = request.user
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
        request.session['pre_2fa_login'] = True
        return redirect('twofa:qr_code' if method == 'qr' else 'twofa:verify_2fa')
    return render(request, 'twofa/setup_2fa.html')

@login_required
def qr_code(request):
    user = request.user
    totp_device = TOTPDevice.objects.get(user=user, name='default')
    secret = totp_device.key
    totp = pyotp.TOTP(secret, interval=60)
    qr_code_url = totp.provisioning_uri(user.email, issuer_name="transcendence")
    google_qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(qr_code_url)}"
    #print("QR Code URL:", google_qr_code_url)
    return render(request, 'twofa/enable_2fa.html', {'qr_code_url': google_qr_code_url})

@login_required
def verify_2fa(request):
    user = request.user
    logger.debug(f"User {user.username} is trying to access verify_2fa page")

    # Check if pre_2fa_login is in session
    if not request.session.get('pre_2fa_login'):
        logger.debug("pre_2fa_login not in session, redirecting to index")
        return redirect('index')

    if request.method == 'POST':
        token = request.POST.get('otp_token')
        user_profile = UserProfile.objects.get(user=user)
        method = user_profile.chosen_2fa_method
        totp = None
        device = None
        logger.debug(f"User {user.username} is trying to verify token for method {method}")
        if method == 'qr':
            device = TOTPDevice.objects.get(user=user, name='default')
            secret = device.key
            totp = pyotp.TOTP(secret, interval=60)
        elif method == 'sms':
            device = TwilioSMSDevice.objects.get(user=user)
            secret = device.key
            totp = pyotp.TOTP(secret, interval=60)
        elif method == 'email':
            device = EmailOTPDevice.objects.get(user=user)
            secret = device.key
            totp = pyotp.TOTP(secret, interval=60)

        current_token = totp.now()
        logger.debug(f"Expected token: {current_token}, User provided token: {token}")

        if totp.verify(token, valid_window=1):
            request.session['2fa_verified'] = True
            logger.info(f"Token verified for user {user.username}")
            if device and not device.confirmed:
                device.confirmed = True
                device.save()
            if 'pre_2fa_login' in request.session:
                del request.session['pre_2fa_login']
            return redirect('index')
        else:
            logger.warning(f"Invalid token for user {user.username}. Expected token: {current_token}, User provided token: {token}")
            #messages.error(request, 'Invalid token. Please try again.')
            return render(request, 'twofa/verify_2fa.html', {'error': 'Invalid token'})
    return render(request, 'twofa/verify_2fa.html')

@login_required
def setup_sms_2fa(request):
    user = request.user
    logger.debug(f"User {user.username} is setting up SMS 2FA")

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if not TwilioSMSDevice.objects.filter(user=user).exists():
            secret = pyotp.random_base32()
            TwilioSMSDevice.objects.create(user=user, phone_number=phone_number, key=secret)
        user.userprofile.chosen_2fa_method = 'sms'
        user.userprofile.save()
        request.session['pre_2fa_login'] = True
        return redirect('twofa:send_sms_token')
    return render(request, 'twofa/setup_sms_2fa.html')

@login_required
def send_sms_token(request):
    user = request.user
    sms_device = TwilioSMSDevice.objects.get(user=user)
    sms_device.generate_token()
    logger.debug(f"Generated SMS token for user {user.username}")
    return redirect('twofa:verify_2fa')

@login_required
def setup_email_2fa(request):
    user = request.user
    logger.debug(f"User {user.username} is setting up Email 2FA")

    if request.method == 'POST':
        if not EmailOTPDevice.objects.filter(user=user).exists():
            secret = pyotp.random_base32()
            EmailOTPDevice.objects.create(user=user, key=secret)
        user.userprofile.chosen_2fa_method = 'email'
        user.userprofile.save()
        request.session['pre_2fa_login'] = True
        return redirect('twofa:send_email_token')
    return render(request, 'twofa/setup_email_2fa.html', {'email': user.email})

@login_required
def send_email_token(request):
    user = request.user
    email_device = EmailOTPDevice.objects.get(user=user)
    email_device.generate_token()
    logger.debug(f"Generated email token for user {user.username}")
    return redirect('twofa:verify_2fa')
