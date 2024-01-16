from .view.auth42 import oauth2_login
from .view.auth42 import oauth2_callback
from .view.profile import ProfileView
from .view.home import HomeView
from .view.register import RegistrationView
from .view.chat import ChatView
from django.shortcuts import render


def pong_game_view(request):
    template_name = 'pong.html'
    return render(request, template_name=template_name, context={})
