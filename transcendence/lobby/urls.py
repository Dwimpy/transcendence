from django.urls import path
from .views import LobbyView
from .views import RoomView

urlpatterns = [
    path('', LobbyView.as_view(), name='lobby'),
    path('<str:room_name>/', RoomView.as_view(), name='room')
]