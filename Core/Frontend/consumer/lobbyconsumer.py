import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from Frontend.model.lobbyroom import LobbyRoom


class LobbyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = "group_lobby"
        await self.accept()
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_new_room",
                "room_data": "wtf",
            }
        )

    async def broadcast_new_room(self, event):
        # room_data = event['room_data']
        # print(room_data)
        print("WTF")
        await self.send(text_data=json.dumps({
            'type': 'new_room',
            'room': 'dfgdfg',
        }))
