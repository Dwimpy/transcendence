from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.functional import lazy
from django.utils.translation import gettext
from .models import AccountUser

class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search for users', max_length=150)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields = ['nickname', 'email', 'picture', 'bio']


gettext_lazy = lazy(gettext, str)


class RegistrationForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ['username', 'nickname', 'email', 'picture', 'bio']

    username = forms.CharField(max_length=150,
                               min_length=1,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               required=True,
                               label="Username")

    nickname = forms.CharField(max_length=150, min_length=1)

    email = forms.EmailField(max_length=255,
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
                          label="Bio")
