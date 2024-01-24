from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from psycopg2.extensions import JSON

from .lobbyconsumer import LobbyConsumer
from ..models.lobby import Lobby
from ..models.customuser import CustomUser
import json


class RoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.channel_layer.group_add(
            "group_lobby",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        pass

    async def create_new_room(self):
        # Your logic to create a new room goes here
        # new_room = LobbyRoom.objects.get(name='random name')
        # After creating the room, notify the lobby about the new room
        await self.channel_layer.group_send(
            "group_lobby",
            {
                'type': 'broadcast_new_room',
                'room_data': {
                    # 'name': new_room.name,
                    # # 'username': new_room.user.username,
                    # 'player_count': new_room.player_count,
                    # 'is_room_full': new_room.is_room_full,
                    'name': 'fuck you'
                },
            }
        )