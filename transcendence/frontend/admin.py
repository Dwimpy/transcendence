from django.contrib import admin
from .models.customuser import CustomUser
from .models.room import Room
from .models.lobby import Lobby

# Register your models here.
admin.register(CustomUser)
admin.register(Room)
admin.register(Lobby)
