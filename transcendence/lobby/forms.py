from django import forms
from .models import Rooms


class RoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['room_name']

    room_name = forms.CharField(max_length=150, required=True)
