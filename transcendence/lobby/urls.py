from django.urls import path
from .views import LobbyView
from .views import RoomView
from .views import SelectView

urlpatterns = [
    path('', SelectView.as_view(), name='select'),
    path('<str:game_lobby>/', LobbyView.as_view(), name='lobby'),
    path('<str:game_lobby>/<str:room_name>/', RoomView.as_view(), name='room'),
    # path('<str:room_name>/', RoomView.as_view(), name='room')
]