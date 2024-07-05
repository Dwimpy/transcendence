from django.urls import path
from .views import GameView

urlpatterns = [
    path('<str:game_lobby>/<str:room_name>/<int:game_id>', GameView.as_view(), name='game'),

]