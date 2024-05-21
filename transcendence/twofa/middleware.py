from django.shortcuts import redirect
from django.urls import reverse

class TwoFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_profile = getattr(request.user, 'userprofile', None)
            if user_profile and user_profile.chosen_2fa_method:
                if not request.session.get('2fa_verified', False):
                    allowed_paths = [
                        reverse('twofa:verify_2fa'),
                        reverse('twofa:send_sms_token'),
                        reverse('twofa:setup_2fa'),
                        reverse('twofa:setup_sms_2fa'),
                        reverse('twofa:setup_email_2fa'),
                        reverse('logout'),
                    ]
                    if request.path not in allowed_paths:
                        return redirect('twofa:verify_2fa')
        response = self.get_response(request)
        return response
