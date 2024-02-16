from django.urls import path

from .consumers import LobbyConsumer

websocket_urlpatterns = [
    path(r"ws/lobby", LobbyConsumer.as_asgi()),
]