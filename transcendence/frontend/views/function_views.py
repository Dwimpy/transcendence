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
    lobby, created = Lobby.objects.get_or_create(pk=1)
    lobby.create_room()
    rooms = lobby.rooms.all()
    print(rooms)
    return render(request, template_name, {'rooms': rooms})


def pong_room(request):
    template_name = 'frontend/pong_room.html'
    lobby, created = Lobby.objects.get_or_create(pk=1)
    lobby.create_room()
    return render(request, template_name, {})


def create_room(request, form=None):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('index')
    else:
        form = form
    return request, 'frontend/create_room.html', {'form': form}
