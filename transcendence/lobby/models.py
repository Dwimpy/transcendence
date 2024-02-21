from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from accounts.models import AccountUser
from channels.db import database_sync_to_async


class Rooms(models.Model):
    room_name = models.CharField(max_length=150, unique=True)
    assigned_users = models.ManyToManyField(AccountUser,
                                            related_name='assigned_room',
                                            blank=True)
    player_count = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)

    def add_user_to_room(self, user):
        self.assigned_users.add(user)

    def remove_user_from_room(self, user):
        self.assigned_users.remove(user)

    @staticmethod
    def is_user_assigned(user):
        return Rooms.objects.filter(assigned_users=user).exists()

    @staticmethod
    def update_rooms():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'lobby',
            {
                'type': 'update_rooms'
            }
        )
