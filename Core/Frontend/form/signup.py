from django import forms
from ..model.customuser import CustomUser
from allauth.account.forms import SignupForm


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

