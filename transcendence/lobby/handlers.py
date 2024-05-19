from asyncio import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from lobby.constants import LOBBY_WS_GROUP_NAME, ROOMS_WS_GROUP_NAME
from .models import Rooms


def send_message_to_consumer(consumer_channel, action_type, action):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        consumer_channel,
        {
            'type': action_type,
            'message': action
        }
    )


def update_room_and_lobby(action: str, room: Rooms):
    send_message_to_consumer(LOBBY_WS_GROUP_NAME, 'update_lobby_view', action)
    send_message_to_consumer(ROOMS_WS_GROUP_NAME + room.room_name, 'update_room_view', action)


def room_created_handler(sender, action, **kwargs):
    room = Rooms.objects.get(room_name=kwargs.get("room_name"))
    room.add_user_to_room(user=kwargs.get("user"))
    update_room_and_lobby(action, room)


def user_joined_a_room_handler(sender, action, **kwargs):
    try:
        room = Rooms.objects.get(room_name=kwargs.get("room_name"))
        user = kwargs.get("user")
        if not room.assigned_users.filter(pk=user.username).exists():
            room.add_user_to_room(user)
        update_room_and_lobby(action, room)
    except Rooms.DoesNotExist as e:
        pass


def user_left_a_room_handler(sender, action, **kwargs):
    try:
        room = Rooms.objects.get(room_name=kwargs.get("room_name"))
        room_name = room.room_name
        user = kwargs.get("user")
        if room.assigned_users.filter(pk=user.username).exists():
            room.remove_user_from_room(user)
        if Rooms.objects.filter(room_name=room_name).exists():
            send_message_to_consumer(ROOMS_WS_GROUP_NAME + room.room_name, 'update_room_view', action)
        send_message_to_consumer(LOBBY_WS_GROUP_NAME, 'update_lobby_view', action)
    except Rooms.DoesNotExist as e:
        pass


def delete_room_handler(sender, action, **kwargs):
    try:
        room = Rooms.objects.get(room_name=kwargs.get("room_name"))
        room.delete()
        send_message_to_consumer(LOBBY_WS_GROUP_NAME, 'update_lobby_view', action)
    except Rooms.DoesNotExist as e:
        pass
