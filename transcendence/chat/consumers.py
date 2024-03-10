from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'chat',
            self.channel_name,
        )
        await self.accept()

    async def receive_json(self, text_data=None, bytes_data=None):
        print(text_data)
        print(text_data['message'])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'chat',
            self.channel_name,
        )
