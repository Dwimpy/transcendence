from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db.models import Q

from .models import PrivateConversation, Messages
from accounts.models import AccountUser
from django.contrib.contenttypes.models import ContentType


def message_sent_handler(sender, data, **kwargs):
    user = AccountUser.objects.get(username=data['values']['user'])
    other = AccountUser.objects.get(username=data['values']['other'])

    conversation = PrivateConversation.objects.filter(
        Q(user1=user, user2=other) | Q(user1=other, user2=user)
    ).first()

    if not conversation:
        conversation = PrivateConversation.objects.create(
            user1=user, user2=other
        )
        conversation = PrivateConversation.objects.filter(
            Q(user1=user, user2=other) | Q(user1=other, user2=user)
        ).first()
    content_type = ContentType.objects.get_for_model(conversation)
    Messages.objects.create(content_type=content_type,
                            object_id=conversation.pk,
                            sender=user,
                            content=data['message'])

    channel_layer = get_channel_layer()
    data = {'type': content_type, 'id': conversation.pk}
    async_to_sync(channel_layer.group_send)(
        f'chat_{conversation.pk}',
        {
            'type': 'update_chat',
            'message': data
        }
    )



def user_connected_handler(sender, user1, user2, **kwargs):

    user = AccountUser.objects.get(username=user1)
    other = AccountUser.objects.get(username=user2)

    conversation = PrivateConversation.objects.filter(
        Q(user1=user, user2=other) | Q(user1=other, user2=user)
    ).first()

    if not conversation:
        conversation = PrivateConversation.objects.create(
            user1=user, user2=other
        )
        conversation = PrivateConversation.objects.filter(
            Q(user1=user, user2=other) | Q(user1=other, user2=user)
        ).first()
    return conversation.pk


