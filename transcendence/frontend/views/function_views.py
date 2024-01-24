from .profile import ProfileView
from .home import HomeView
from .register import RegistrationView
from .chat import ChatView
from django.shortcuts import render, redirect
from ..models.lobby import Lobby
from ..forms.room import RoomForm


def pong_menu(request):
    template_name = 'frontend/pong_menu.html'
    user = request.user
    if user.is_authenticated:
        return render(request, template_name)
    else:
        return redirect('login')


def pong_lobby(request):
    template_name = 'frontend/pong_lobby.html'
    return render(request, template_name)


def game_lobby(request):
    template_name = 'frontend/game/game_lobby.html'
    lobby, created = Lobby.objects.get_or_create(pk=1)
    rooms = lobby.rooms.all()
    print(rooms)
    return render(request, template_name, {'rooms': rooms})


def pong_room(request):
    template_name = 'frontend/pong_room.html'
    return render(request, template_name, {})


def create_room(request):
    form = RoomForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            redirect('index')
    else:
        redirect('create_room')
    return render(request, 'frontend/game/create_room.html', {'form': form})
