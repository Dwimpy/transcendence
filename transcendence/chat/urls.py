from django.urls import path
from .views import ChatView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('<str:first_name>', ChatView.as_view(), name='chat-with')
]