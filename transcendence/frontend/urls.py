from django.urls import path, include, re_path

from django.contrib.auth import views as auth_views
from .views.register import RegistrationView
from .views.profile import ProfileView
from .views.home import HomeView
from .views.chat import ChatView
from .views.function_views import pong_menu, pong_lobby, pong_room, create_room, game_lobby

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('chat', ChatView.as_view(), name='chat'),
    path('menu', pong_menu, name='game_menu'),
    re_path(r'lobby/?$', pong_lobby, name='pong_lobby'),
    re_path(r'lobby/game_lobby?$', game_lobby, name='game_lobby'),
    re_path('lobby/create_room/?$', create_room, name='create_room'),
    # path('lobby', pong_room, name='game_room'),
    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('accounts/signup', RegistrationView.as_view(), name='signup'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
]

