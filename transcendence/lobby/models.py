
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.http import HttpResponse
from django.urls import reverse_lazy

from accounts.models import AccountUser
from channels.db import database_sync_to_async

from lobby.constants import LOBBY_WS_GROUP_NAME


class Rooms(models.Model):
    room_name = models.CharField(max_length=150, unique=True)
    assigned_users = models.ManyToManyField(AccountUser,
                                            related_name='assigned_room',
                                            blank=True)
    player_count = models.IntegerField(default=0)
    type = models.CharField(max_length=150, blank=True)
    is_full = models.BooleanField(default=False)

    def add_user_to_room(self, user):
        self.player_count += 1
        self.assigned_users.add(user)
        if self.player_count == 2:
            self.is_full = True
        self.save()

    def remove_user_from_room(self, user):
        self.player_count -= 1
        self.assigned_users.remove(user)
        if self.player_count == 0:
            self.delete()
        else:
            if self.is_full:
                self.is_full = False
            self.save()

    @database_sync_to_async
    def get_all_rooms(self):
        return Rooms.objects.all()

    @staticmethod
    def is_user_assigned(user):
        return Rooms.objects.filter(assigned_users=user).exists()
