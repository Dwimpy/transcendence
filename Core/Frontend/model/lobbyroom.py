from django.db import models
from Frontend.model.customuser import CustomUser


class LobbyRoom(models.Model):
    class Meta:
        db_table = 'rooms'

    name = models.CharField(max_length=255, null=False, default="")
    # users = models.ManyToManyField(CustomUser, related_name='room_users')
    player_count = models.IntegerField(default=0)
    is_room_full = models.BooleanField(default=False)

    def __str__(self):
        return f'name: {self.name}\nplayer_count: {self.player_count}'
