from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import UserProfile, TwilioSMSDevice, EmailOTPDevice
import pyotp
import logging
import urllib.parse
from binascii import hexlify, unhexlify
from jwtauth.views import issue_jwt as jwt

logger = logging.getLogger(__name__)

@login_required
def setup_2fa(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Disable 2fa
        if 'disable' in request.POST:
            user_profile.chosen_2fa_method = ''
            user_profile.save()
            TOTPDevice.objects.filter(user=user).delete()
            TwilioSMSDevice.objects.filter(user=user).delete()
            EmailOTPDevice.objects.filter(user=user).delete()
            return redirect('index')

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
    
    method_display_map = {
        'qr': 'QR-Code Verification',
        'sms': 'SMS Verification',
        'email': 'Email Verification'
    }
    chosen_method_display = method_display_map.get(user_profile.chosen_2fa_method, '')
    context = {
        'chosen_method': chosen_method_display
    }

    return render(request, 'twofa/setup_2fa.html', context)

@login_required
def qr_code(request):
    user = request.user
    totp_device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
    
    if created:
        secret = pyotp.random_base32()
        hex_key = hexlify(secret.encode('utf-8')).decode('utf-8')
        totp_device.key = hex_key
        totp_device.save()
    else:
        hex_key = totp_device.key
        try:
            int(hex_key, 16)
        except ValueError:
            secret = hex_key
            hex_key = hexlify(secret.encode('utf-8')).decode('utf-8')
            totp_device.key = hex_key
            totp_device.save()
        else:
            secret = unhexlify(hex_key).decode('utf-8')
    secret = unhexlify(hex_key).decode('utf-8')
    totp = pyotp.TOTP(secret, interval=60)
    qr_code_url = totp.provisioning_uri(user.email, issuer_name="transcendence")
    google_qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(qr_code_url)}"
    return render(request, 'twofa/enable_2fa.html', {
        'qr_code_url': google_qr_code_url,
        'auth_app_info': 'Scan this QR code with Google Authenticator.'
    })

@login_required
def verify_2fa(request):
    user = request.user
    logger.debug(f"User {user.username} is trying to access verify_2fa page")

    # Check if pre_2fa_login is in session
    if not request.session.get('pre_2fa_login'):
        logger.debug("pre_2fa_login not in session, redirecting to index")
        return redirect('index')

    user_profile = UserProfile.objects.get(user=user)
    method = user_profile.chosen_2fa_method
    method_detail = ""

    if method == 'qr':
        method_detail = "Check your Google Authenticator appp"
    elif method == 'sms':
        device = TwilioSMSDevice.objects.get(user=user)
        method_detail = f"Check your phone number {device.phone_number[:3]}****{device.phone_number[-2:]}"
    elif method == 'email':
        method_detail = f"Check your email {user.email[0]}****@{user.email.split('@')[1]}"

    if request.method == 'POST':
        token = request.POST.get('otp_token')
        totp = None
        device = None
        logger.debug(f"User {user.username} is trying to verify token for method {method}")
        if method == 'qr':
            device = TOTPDevice.objects.get(user=user, name='default')
            hex_key = device.key
            secret = unhexlify(hex_key).decode('utf-8')
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
            
            # JWT
            jwt(user, request)
            
            return redirect('index')
        else:
            logger.warning(f"Invalid token for user {user.username}. Expected token: {current_token}, User provided token: {token}")
            return render(request, 'twofa/verify_2fa.html', {'error': 'Invalid token', 'method_detail': method_detail})
    return render(request, 'twofa/verify_2fa.html', {'method_detail': method_detail})

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
