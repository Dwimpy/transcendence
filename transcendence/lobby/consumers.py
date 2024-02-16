import json
from typing import Dict
from typing import Any

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from django.template.loader import get_template
from .constants import LOBBY_WS_GROUP_NAME
from .forms import RoomForm
from .models import Rooms


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )
        print('connected')
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            LOBBY_WS_GROUP_NAME,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print('received')
        text_data_json = json.loads(text_data)
        room_name = text_data_json['room_name']
        new_room = await Rooms.objects.aget_or_create(room_name=room_name)
        rooms = [room async for room in Rooms.objects.all()]
        html = get_template('lobby/lobby_room_partial_update.html').render(context={'rooms': rooms})
        await self.channel_layer.group_send(
            LOBBY_WS_GROUP_NAME,
            {
                'type': 'update_rooms',
                'html': html
            }
        )

    async def update_rooms(self, event):
        print(event['html'])
        await self.send(text_data=event['html'])

    def created_room(self, event: Dict[str, Any]):
        html = get_template(
            "lobby/lobby_room_partial.html",
        ).render(
            context={
                "rooms": [
                    event["message"],
                ]
            }
        )
        self.send(text_data=html)
