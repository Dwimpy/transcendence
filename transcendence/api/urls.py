from django.urls import path
from api.views import RoomListAPIView, CreateRoomAPIView

urlpatterns = [
    path('room-list/', RoomListAPIView.as_view(), name='room-list'),
    path('create-room/', CreateRoomAPIView.as_view(), name='create-room'),

    # Add other URL patterns if needed
]