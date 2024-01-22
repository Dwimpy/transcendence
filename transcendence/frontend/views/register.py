import requests
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from ..forms.signup import AllAuthSignupForm
from django.shortcuts import redirect
from django.contrib.auth import login
from ..models.customuser import CustomUser
from allauth.account.views import SignupView
from django.core.files.base import ContentFile


class RegistrationView(SignupView):
    template_name = 'frontend/register.html'
    model = CustomUser
    form_class = AllAuthSignupForm

    def form_valid(self, form):
        return super().form_valid(form)


