from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r"ws/chat", ChatConsumer.as_asgi()),
    path(r"ws/chat/", ChatConsumer.as_asgi()),
    path(r"ws/chat/<other_name>", ChatConsumer.as_asgi()),
]