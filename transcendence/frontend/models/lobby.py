from django.core.exceptions import ValidationError
from django.db import models
from .room import Room


class Lobby(models.Model):
    class Meta:
        app_label = 'frontend'
        db_table = 'lobby'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    rooms = models.ManyToManyField(Room)

    def get_rooms(self):
        return self.rooms.all()

    def create_room(self):
        room = Room()
        room.name = 'Hi'
        room.player_count = 0
        room.is_room_full = True
        room.save()
        self.rooms.add(room)
        self.save()
