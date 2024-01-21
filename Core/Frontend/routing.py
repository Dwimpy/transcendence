from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from Frontend.consumer.pongconsumer import PongConsumer
from Frontend.consumer.lobbyconsumer import LobbyConsumer
from Frontend.consumer.roomconsumer import RoomConsumer


websocket_urlpatterns = [
    re_path(r'ws/pong', PongConsumer.as_asgi()),
    re_path(r'ws/lobby', LobbyConsumer.as_asgi()),
    re_path(r'ws/room', RoomConsumer.as_asgi())
]
