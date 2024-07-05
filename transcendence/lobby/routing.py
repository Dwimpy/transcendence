from django.urls import path

from .consumers import LobbyConsumer, RoomConsumer

websocket_urlpatterns = [
    path(r"ws/lobby/<game_room>", LobbyConsumer.as_asgi()),
    path(r"ws/rooms/<room_name>", RoomConsumer.as_asgi()),
    path(r"ws/rooms/<room_name>/test", RoomConsumer.as_asgi()),
    # path(r"ws/lobby/<str:game_lobby>/<str:room_name>/", RoomConsumer.as_asgi()),
]