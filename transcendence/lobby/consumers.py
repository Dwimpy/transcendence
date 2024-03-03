import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import redirect
from django.template.loader import get_template, render_to_string
from .constants import LOBBY_WS_GROUP_NAME, ROOMS_WS_GROUP_NAME
from .forms import RoomForm
from .models import Rooms


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

    async def update_rooms(self, event):
        rooms = [room async for room in Rooms.objects.all()]
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
        await self.room_action('update_room', 'Room ' + self.room_name + ' updated')
        await self.accept()

    async def disconnect(self, close_code):
        try:
            room = await Rooms.objects.aget(room_name=self.room_name)
            if room:
                await self.room_action('update_room', 'Room ' + self.room_name + ' updated')
                await self.channel_layer.group_discard(
                    self.group_room_name,
                    self.channel_name,
                )
        except Rooms.DoesNotExist as e:
            print(str(e))

    async def room_action(self, update_type, message):
        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': update_type,
                'message': message
            }
        )

    async def update_room(self, event):
        try:
            room = await Rooms.objects.aget(room_name=self.room_name)
            html = (get_template('lobby/room_partial_update.html')
                    .render(context={'assigned_users': [user async for user in room.assigned_users.all()],
                                     'room_name': self.room_name,
                                     'room': room}))
            await self.send(text_data=html)
        except Rooms.DoesNotExist as e:
            print(str(e))
