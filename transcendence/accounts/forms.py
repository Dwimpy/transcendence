from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.functional import lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from .models import AccountUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields = ['picture', 'username', 'bio', 'email']


gettext_lazy = lazy(gettext, str)


# class LoginForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,
#     }))
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
#     )