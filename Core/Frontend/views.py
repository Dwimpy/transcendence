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


def pong_lobby(request):
    template_name = 'pong_lobby.html'
    lobby, created = PongLobby.objects.get_or_create(pk=1)
    lobby.create_room()
    rooms = lobby.rooms.all()
    print(rooms)
    return render(request, template_name, {'rooms': rooms})


def pong_room(request):
    template_name = 'pong_room.html'
    lobby, created = PongLobby.objects.get_or_create(pk=1)
    lobby.create_room()
    return render(request, template_name, {})