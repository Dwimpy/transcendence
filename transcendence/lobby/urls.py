from django.urls import path, include
from .views import LobbyView

urlpatterns = [
    path('', LobbyView.as_view(), name='lobby'),
]