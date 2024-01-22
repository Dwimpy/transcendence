from django import forms
from ..models.customuser import CustomUser
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
    picture = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    bio = forms.CharField(max_length=255,
                            min_length=1,
                            widget=forms.TextInput(attrs={'placeholder': 'Bio'}),
                            required=True,
                            label="bio")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

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
