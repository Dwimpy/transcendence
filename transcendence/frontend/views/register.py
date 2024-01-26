import requests
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from django.http import JsonResponse
from ..forms.signup import AllAuthSignupForm
from django.shortcuts import redirect
from django.contrib.auth import login
from ..models.customuser import CustomUser
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile


class RegistrationView(SignupView):
    template_name = 'frontend/register.html'
    model = CustomUser
    form_class = AllAuthSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Welcome, ' + self.request.user.username + '! You are now logged in!')
        return response


