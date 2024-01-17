from .view.profile import ProfileView
from .view.home import HomeView
from .view.register import RegistrationView
from .view.chat import ChatView
from django.shortcuts import render
from .model.ponglobby import PongLobby


def pong_game_view(request):
    template_name = 'pong.html'
    user = request.user
    lobby = PongLobby.objects.get_or_create(name='hello')
    lobby[0].add_to_lobby(user)
    print(lobby)
    return render(request, template_name=template_name, context={'lobby': lobby[0]})
