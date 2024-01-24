import asyncio

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError
from django.db import models
from .room import Room
from django.db import IntegrityError


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

    @staticmethod
    @database_sync_to_async
    def get_or_create_lobby():
        lobby, _ = Lobby.objects.get_or_create(pk=1)
        return lobby

    @database_sync_to_async
    def create_room(self, room_name, user):
        if not Room.room_exists(room_name):
            try:
                # Create the room without adding it to the lobby yet
                new_room = Room.objects.create(name=room_name)
                # Add the user to the room's users
                new_room.users.add(user)
                new_room.player_count = new_room.users.count()
                # Save the room to the database
                new_room.save()
                # Now add the room to the lobby
                self.rooms.add(new_room)
                # Save the lobby to the database
                self.save()
                return new_room
            except IntegrityError as e:
                print(e)
        else:
            print("room already exists")
            return None
