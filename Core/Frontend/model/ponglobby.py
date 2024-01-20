from django.core.exceptions import ValidationError
from django.db import models
from .lobbyroom import LobbyRoom


class PongLobby(models.Model):
    class Meta:
        db_table = 'lobby_rooms'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    rooms = models.ManyToManyField(LobbyRoom)

    def get_rooms(self):
        return self.rooms.all()

    def create_room(self):
        room = LobbyRoom()
        room.name = 'Hi'
        room.player_count = 0
        room.is_room_full = True
        room.save()
        self.rooms.add(room)
        self.save()
