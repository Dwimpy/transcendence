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
    identity_url = 'https://api.intra.42.fr/v2/users'
    redirect_uri_protocol = 'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-4ca9b16084b5a8cc3d3273b6db68ffa56943bf4c7652decc31d30653c4ca1295&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000&response_type=code'

    supports_state = True

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_data(token.token)
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

    def get_data(self, token):
        # Verify the user first
        resp = requests.get(
            self.identity_url,
            params={'token': token}
        )
        resp = resp.json()

        if not resp.get('ok'):
            raise OAuth2Error()

        # Fill in their generic info
        info = {
            'user': resp.get('user'),
        }

        return info


oauth2_login = OAuth2LoginView.adapter_view(FortyTwoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FortyTwoOAuth2Adapter)
