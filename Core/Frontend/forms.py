# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import CustomUser
from allauth.account.forms import SignupForm
# from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'picture', 'bio', 'password1', 'password2']


class AllAuthSignupForm(SignupForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'picture', 'bio', 'password1', 'password2']
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
    bio = forms.CharField(max_length=255,
                            min_length=1,
                            widget=forms.TextInput(attrs={'placeholder': 'Bio'}),
                            required=True,
                            label="bio")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    picture = forms.ImageField()

    def save(self, request):
        bio_value = self.cleaned_data['bio']
        picture_value = self.cleaned_data['picture']
        user = super().save(request)
        user.picture = picture_value
        user.bio = bio_value
        user.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'bio', 'email']
