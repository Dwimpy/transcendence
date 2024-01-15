from django.shortcuts import render
from django.views import View
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from ..provider import FortyTwoProvider
from ..form.signup import AllAuthSignupForm
from django.shortcuts import redirect
from django.contrib.auth import login


class RegistrationView(View):
    template_name = '../templates/register.html'
    index_template = '../templates/home.html'

    def get(self, request, *args, **kwargs):
        form = AllAuthSignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AllAuthSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return render(request, self.index_template)
        return render(request, self.template_name, {'form': form})
