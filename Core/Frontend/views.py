from .view.profile import ProfileView
from .view.home import HomeView
from .view.register import RegistrationView
from .view.chat import ChatView
from django.shortcuts import render, redirect
from .model.ponglobby import PongLobby


def pong_menu(request):
    template_name = 'pong_menu.html'
    user = request.user
    if user.is_authenticated:
        return render(request, template_name)
    else:
        return redirect('login')


