from django import forms
from ..model.customuser import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'bio', 'email']