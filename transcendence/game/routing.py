from django.urls import path
from .consumers import PongConsumer

websocket_urlpatterns = [
    path(r"ws/game/", PongConsumer.as_asgi()),
]