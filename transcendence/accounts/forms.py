from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.functional import lazy
from django.utils.translation import gettext
from .models import AccountUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields = ['picture', 'username', 'bio', 'email']


gettext_lazy = lazy(gettext, str)


class RegistrationForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ['username', 'email', 'bio', 'picture']

    username = forms.CharField(max_length=255,
                               min_length=1,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               required=True,
                               label="Username")
    email = forms.CharField(max_length=255,
                            min_length=1,
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                            required=True,
                            label="Email")
    picture = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    bio = forms.CharField(max_length=255,
                            min_length=1,
                            widget=forms.TextInput(attrs={'placeholder': 'Bio'}),
                            required=True,
                            label="bio")
