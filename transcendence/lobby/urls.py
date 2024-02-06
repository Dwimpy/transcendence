from django.urls import path, include
from .views import LobbyView, RoomProcessView, UpdateRoomsView

urlpatterns = [
    path('', LobbyView.as_view(), name='lobby'),
    path('create_room/', RoomProcessView.as_view(), name='add_room'),
    path('update_rooms/', UpdateRoomsView.as_view(), name='update_rooms')
]