from ..models.room import Room
from django import forms


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
