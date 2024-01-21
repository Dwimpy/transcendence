from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .lobbyconsumer import LobbyConsumer
from Frontend.model.ponglobby import LobbyRoom
from Frontend.model.customuser import CustomUser
import json


class RoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.channel_layer.group_add(
            "group_lobby",
            self.channel_name
        )
        await self.create_new_room()
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Add any disconnect logic if needed

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    @sync_to_async
    def create_lobby_room(self):
        new_room = LobbyRoom().objects.get_or_create(name="random name")
        # user = CustomUser.objects.get('andrei123')
        # new_room.users.add(user)
        new_room.player_count = 1
        new_room.save()

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