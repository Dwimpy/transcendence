from django.urls import path, include

from django.contrib.auth import views as auth_views
from .view.register import RegistrationView
from .view.profile import ProfileView
from .view.home import HomeView
from .view.chat import ChatView
from .views import pong_menu
from .views import pong_lobby
from .views import pong_room

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('chat', ChatView.as_view(), name='chat'),
    path('menu', pong_menu, name='game_menu'),
    path('lobby', pong_lobby, name='game_lobby'),
    path('lobby', pong_room, name='game_room'),
    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('signup', RegistrationView.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]

