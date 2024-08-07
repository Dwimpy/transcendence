import json
from django.contrib.auth import login, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.base import ContentFile
from django.http import Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from .models import AccountUser
from .forms import ProfileForm
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.conf import settings
from urllib.parse import quote
import requests
from django.contrib import messages
from django.conf import settings
from .forms import UserSearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from twofa.models import UserProfile, TwilioSMSDevice, EmailOTPDevice
from django_otp.plugins.otp_totp.models import TOTPDevice
from binascii import unhexlify
import pyotp
from jwtauth.views import JWTAuthMixin
from jwtauth.views import issue_jwt
from django.core.exceptions import PermissionDenied

@login_required
def search_users(request):
    form = UserSearchForm()
    results = []
    if 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = AccountUser.objects.filter(username__icontains=query).exclude(username=request.user.username)
    return render(request, 'accounts/search_users.html', {'form': form, 'results': results})

@login_required
def add_friend(request, username):
    user = request.user
    friend = get_object_or_404(AccountUser, username=username)
    user.friends.add(friend)
    friend.friends.add(user)
    return redirect('profile', username=user.username)

@login_required
def remove_friend(request, username):
    user = request.user
    friend = get_object_or_404(AccountUser, username=username)
    user.friends.remove(friend)
    friend.friends.remove(user)
    return redirect('profile', username=user.username)

@login_required
def profile(request, username):
    user = get_object_or_404(AccountUser, username=username)
    is_friend = request.user.friends.filter(username=username).exists()
    return render(request, 'accounts/profile.html', {'user': user, 'is_friend': is_friend})

@login_required
def profile_view(request, username):
    user = get_object_or_404(AccountUser, username=username)
    history = user.history.get('tictac', [])

    context = {
        'user': user,
        'history': history,
        # Add other context variables if needed
    }
    return render(request, 'accounts/profile.html', context)

class ProfileView(JWTAuthMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = AccountUser
    form_class = ProfileForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            username = self.kwargs.get('username')
            logged_user = request.user

            if logged_user.username != username:
                raise PermissionDenied("You do not have permission to access this profile.")

            user = self.get_object()
            form = self.form_class(instance=user)
            search_form = UserSearchForm()

            search_results = []
            if 'query' in self.request.GET:
                search_form = UserSearchForm(self.request.GET)
                if search_form.is_valid():
                    query = search_form.cleaned_data['query']
                    search_results = AccountUser.objects.filter(username__icontains=query).exclude(username=request.user.username)

            if logged_user.username != user.username:
                for field in form.fields:
                    form.fields[field].widget.attrs['readonly'] = True

            context = {
                'user': user,
                'logged_user': logged_user.username,
                'form': form,
                'search_form': search_form,
                'search_results': search_results,
                'third_party_auth': user.third_party_auth,
            }

            return render(self.request, self.template_name, context)
        except AccountUser.DoesNotExist:
            raise Http404("User does not exist")

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('profile', args=[user.username])

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """
        Security check complete. Log the user in.
        """
        user = form.get_user()
        login(self.request, user)
        try:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.chosen_2fa_method:
                self.request.session['pre_2fa_login'] = True
                method = user_profile.chosen_2fa_method

                if method == 'qr':
                    totp_device = TOTPDevice.objects.get(user=user, name='default')
                    hex_key = totp_device.key
                    secret = unhexlify(hex_key).decode('utf-8')
                    totp = pyotp.TOTP(secret, interval=60)

                elif method == 'sms':
                    sms_device = TwilioSMSDevice.objects.get(user=user)
                    sms_device.generate_token()

                elif method == 'email':
                    email_device = EmailOTPDevice.objects.get(user=user)
                    email_device.generate_token()

                return redirect('twofa:verify_2fa')
        except UserProfile.DoesNotExist:
            pass
        
        # JWT
        issue_jwt(user, self.request)

        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('profile', args=[user.username])

class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user=user)
        
        issue_jwt(user, self.request)
        
        return super().form_valid(form)

class FortyTwoAuthView(View):

    def get(self, request):
        authorize_url = 'https://api.intra.42.fr/oauth/authorize'
        redirect_uri = quote(settings.REDIRECT_URI, safe='')
        scope = 'public'
        response_type = 'code'
        return redirect(f'{authorize_url}?'
                        f'client_id={settings.CLIENT_ID}&'
                        f'redirect_uri={redirect_uri}&'
                        f'response_type={response_type}&'
                        f'scope={scope}')


class UserDataFetchError(Exception):
    """Exception raised when failing to fetch user data."""

    def __init__(self, message="Failed to fetch user data"):
        self.message = message
        super().__init__(self.message)


class AccessTokenException(Exception):
    """Exception raised when failing to fetch user data."""

    def __init__(self, message="Invalid access token"):
        self.message = message
        super().__init__(self.message)


class FortyTwoAuthCallbackView(View):

    def __init__(self, *args, **kwargs):
        self.access_token = None
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.access_token = FortyTwoAuthCallbackView.get_auth_token(request)
        return self.authenticate_or_create_user(request)

    @staticmethod
    def get_auth_token(request):
        token_url = 'https://api.intra.42.fr/oauth/token'
        code = request.GET.get('code')
        if code:
            token_data = {
                'grant_type': 'authorization_code',
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET,
                'redirect_uri': settings.REDIRECT_URI,
                'code': request.GET.get('code')
            }
            try:
                response = requests.post(token_url, data=token_data,
                                         headers={
                                             'Content-Type': 'application/x-www-form-urlencoded'
                                         })
                response.raise_for_status()
                token = response.json().get('access_token')
                if token:
                    return token
                else:
                    messages.info(request, response.json().get('error_message', 'Failed to get access token'))
            except AccessTokenException as e:
                messages.error(request, f'{str(e)}')
        return None

    def get_user_data(self, request):
        profile_url = 'https://api.intra.42.fr/v2/me'
        try:
            user_data = requests.get(profile_url,
                                     headers={
                                         'Authorization': f'Bearer {self.access_token}'
                                     })
            user_data.raise_for_status()
            return user_data
        except UserDataFetchError as e:
            messages.error(request, str(e))

    def authenticate_or_create_user(self, request):
        if self.access_token:
            user_data = self.get_user_data(request)
            if user_data.status_code == 200:
                try:
                    user_data = user_data.json()
                    user_login = user_data['login']
                    user_nickname = user_data['displayname']
                    user_email = user_data['email']
                    user_bio = user_data['kind']
                    if user_login and user_nickname and user_email and user_bio:
                        user, created = AccountUser.objects.get_or_create(username=user_login,
                                                                          nickname=user_nickname,
                                                                          email=user_email,
                                                                          bio=user_bio,
                                                                          third_party_auth=True)

                        if created:
                            user_image_url = user_data['image']['versions']['large']
                            if user_image_url:
                                user_image = requests.get(user_image_url)
                                if user_image.status_code == 200:
                                    user_image_content = user_image.content
                                    file_name = f'{user.username}_profile_pic.jpg'
                                    user.picture.save(name=file_name, content=ContentFile(user_image_content),
                                                      save=True)
                        login(request, user)
                        messages.success(request, f'Welcome, {user.username}')

                        # JWT
                        issue_jwt(user, request)
                    
                        response = redirect('profile', user.username)
                        return response
                    else:
                        messages.error(request, 'Incomplete user data received')
                except json.JSONDecodeError:
                    messages.error(request, 'Failed to parse user data')
            else:
                messages.error(request, 'Failed to parse user data from API')
        else:
            messages.info(request, 'Invalid authorization code')
        return redirect('login')
