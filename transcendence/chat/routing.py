from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r"ws/chat", ChatConsumer.as_asgi()),
]