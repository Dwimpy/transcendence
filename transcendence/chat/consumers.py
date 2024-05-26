from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

from django.db.models import Q
from django.template.loader import get_template

from accounts.models import AccountUser
from .models import PrivateConversation, Messages
from .signals import message_sent, user_connected


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = "NORMAL"
        self.user = ""
        self.other = ""
        self.message = None

    async def connect(self):
        self.user = self.scope['user']
        self.other = self.scope['url_route']['kwargs']['other_name'] if 'other_name' in self.scope['url_route'][
            'kwargs'] else ""
        if self.other:
            test = await sync_to_async(user_connected.send)(
                sender=self,
                user1=self.user,
                user2=self.other
            )
            self.name = f'chat_{test[0][1]}'
            await self.channel_layer.group_add(
                self.name,
                self.channel_name,
            )
        await self.accept()

    async def receive_json(self, text_data=None, bytes_data=None):
        await sync_to_async(message_sent.send)(
            sender=self,
            data=text_data
        )

        # await self.channel_layer.group_send(
        #     self.name,
        #     {
        #         'type': 'update_chat',
        #         'message': messages[0][1]
        #     }
        # )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.name}',
            self.channel_name,
        )

    async def update_chat(self, event):
        msg = [msg async for msg in Messages.objects.filter(content_type=event['message']['type'], object_id=event['message']['id']).order_by('sent_at').select_related('sender')]
        context = {'user': self.user, 'other': self.other, 'hidden': "", 'messages': msg}
        html = (get_template('chat/chat_partial_update.html')
                .render(context=context))
        await self.send(text_data=html)
