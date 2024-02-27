import json
from typing import Dict
from typing import Any

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from django.shortcuts import redirect
from django.template.loader import get_template, render_to_string
from .constants import LOBBY_WS_GROUP_NAME, ROOMS_WS_GROUP_NAME
from .forms import RoomForm
from .models import Rooms


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if 'room_name' in text_data_json:
            room_name = text_data_json['room_name']
            new_room, created = await Rooms.objects.aget_or_create(room_name=room_name)
        if text_data_json['HEADERS']['HX-Trigger'] == 'key-up':
            print('hello')

    async def update_rooms(self, event):
        rooms = [room async for room in Rooms.objects.all()]
        html = get_template('api/lobby_room_partial_update.html').render(context={'rooms': rooms})
        await self.send(text_data=html)


class RoomConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self):
        self.room_name = None
        self.group_room_name = None
        super().__init__(self)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_room_name = ROOMS_WS_GROUP_NAME + self.room_name
        room = await Rooms.objects.aget(room_name=self.room_name)
        await sync_to_async(room.add_user_to_room)(self.scope['user'])
        await self.channel_layer.group_add(
            self.group_room_name,
            self.channel_name,
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'world',
                'message': 'what the fuck'
            }
        )

    async def disconnect(self, close_code):
        room = await Rooms.objects.aget(room_name=self.room_name)
        await sync_to_async(room.remove_user_from_room)(self.scope['user'])
        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'world',
                'message': 'what the fuck'
            }
        )
        await self.channel_layer.group_discard(
            self.group_room_name,
            self.channel_name,
        )

    async def world(self, event):
        room = await Rooms.objects.aget(room_name=self.room_name)
        html = (get_template('lobby/room_partial_update.html')
                .render(context={'assigned_users': [user async for user in room.assigned_users.all()], 'room_name': self.room_name}))
        await self.send(text_data=html)

