from django.urls import path, include
from .views import lobby_view

urlpatterns = [
    path('', lobby_view, name='lobby')
]