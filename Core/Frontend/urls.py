from django.urls import path, include

from django.contrib.auth import views as auth_views
from .view.register import RegistrationView
from .view.profile import ProfileView
from .view.home import HomeView
from .view.chat import ChatView
from .views import pong_menu

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('chat', ChatView.as_view(), name='chat'),
    path('game/pong', pong_menu, name='pong'),
    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('accounts/signup', RegistrationView.as_view(), name='signup'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
]

