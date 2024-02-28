from django.urls import path
from api.views import RoomListAPIView, CreateRoomAPIView
from . import views

urlpatterns = [
    path('', views.APIView.as_view(), name='api-root'),
    path('room-list/', RoomListAPIView.as_view(), name='room-list'),
    path('create-room/', CreateRoomAPIView.as_view(), name='create-room'),

    # Add other URL patterns if needed
]