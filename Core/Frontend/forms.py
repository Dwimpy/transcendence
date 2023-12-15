# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
