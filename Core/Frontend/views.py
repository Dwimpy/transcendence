from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import AllAuthSignupForm
from allauth.account.auth_backends import AuthenticationBackend as AllauthBackend

def register(request):
    if request.method == 'POST':
        form = AllAuthSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect('index')  # Redirect to the home page after successful registration
    else:
        form = AllAuthSignupForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})


def text(response):
    return render(response, "text.html", {})


def home(response):
    return render(response, "home.html", {})


import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from allauth.socialaccount.providers.oauth2.client import OAuth2Error

from .provider import FortyTwoProvider


class FortyTwoOAuth2Adapter(OAuth2Adapter):
    provider_id = FortyTwoProvider.id

    access_token_url = 'https://api.intra.42.fr/oauth/token'
    authorize_url = 'https://api.intra.42.fr/oauth/authorize'
    profile_url = 'https://api.intra.42.fr/v2/me'
    redirect_uri_protocol = 'http'  # Update this to 'https' if your site uses HTTPS
    redirect_uri = '127.0.0.1:8000/42/login/callback'
    # identity_url = '127.0.0.1:8000/42/login/callback'
    # redirect_uri_protocol = 'http://127.0.0.1:8000/login/callback'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)

oauth2_login = OAuth2LoginView.adapter_view(FortyTwoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoOAuth2Adapter)
