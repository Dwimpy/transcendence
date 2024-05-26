import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import redirect
from django.template.loader import get_template, render_to_string
from .constants import LOBBY_WS_GROUP_NAME, ROOMS_WS_GROUP_NAME
from .forms import RoomForm
from .models import Rooms
from channels.db import database_sync_to_async

from .signals import user_left_a_room
from .views import RoomView


class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        print(data_json)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )

    async def update_lobby_view(self, event):
        rooms = await database_sync_to_async(list)(Rooms.objects.all())
        html = get_template('lobby/lobby_room_partial_update.html').render(context={'rooms': rooms})
        await self.send(text_data=html)


class RoomConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        self.room_name = None
        self.group_room_name = None
        super().__init__(self)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_room_name = ROOMS_WS_GROUP_NAME + self.room_name
        await self.channel_layer.group_add(
            self.group_room_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        await sync_to_async(user_left_a_room.send)(
            sender=RoomView,
            action=f"{user.username} has left room {self.room_name}",
            room_name=self.room_name,
            user=user
        )
        await self.channel_layer.group_discard(
            ROOMS_WS_GROUP_NAME + self.room_name,
            self.channel_name,
        )

    async def update_room_view(self, event):
        try:
            room = await Rooms.objects.aget(room_name=self.room_name)
            assigned_users = await database_sync_to_async(list)(room.assigned_users.all())
            html = (get_template('lobby/room_partial_update.html')
                    .render(context={'room': room,
                                     'assigned_users': assigned_users
                                     }))
            await self.send(text_data=html)
        except Rooms.DoesNotExist as e:
            print(str(e))
