import json
from time import sleep

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib import messages

from accounts.models import AccountUser
from .models import Rooms
from .forms import RoomForm
from .signals import room_created, user_joined_a_room, user_left_a_room, start_game
from .signals import delete_room


# Create your views here.

def is_htmx(request):
    return request.META.get('HTTP_HX_REQUEST') is not None


class SelectView(LoginRequiredMixin, TemplateView):
    template_name = 'lobby/select_game.html'
    model = Rooms

    def get(self, request, *args, **kwargs):
        if is_htmx(request):
            lobby = reverse_lazy('lobby', args=[request.headers.get('HX-Target')])
            return HttpResponse(
                status=200,
                headers={
                    'HX-Redirect': lobby,
                }
            )
        return render(request, self.template_name)


class LobbyView(LoginRequiredMixin, TemplateView):
    model = Rooms
    form_class = RoomForm
    template_name = 'lobby/lobby.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        game_name = kwargs['game_lobby']
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')
            if hx_target == 'dialog':
                context['field_name'] = 'room_name'
                context['form'] = RoomForm()
                return render(request, 'lobby/lobby_form.html', context)
            elif hx_target == 'join-room-btn':
                return LobbyView.join_room(request, kwargs['game_lobby'])
            elif hx_target == 'delete-room-btn':
                return LobbyView.delete_room(room_name=request.GET.get("room-name"))
        return render(request, self.template_name, context)

    @staticmethod
    def delete_room(room_name: str):
        delete_room.send(
            sender=LobbyView,
            action=f"Room {room_name} has been deleted",
            room_name=room_name
        )
        return HttpResponse(status=204)

    def post(self, request, *args, **kwargs):
        form = RoomForm(request.POST)
        game_name = kwargs['game_lobby']
        # if is_htmx(request):
        #     hx_target = request.headers.get('HX-Target')
        if form.is_valid():
            return LobbyView.create_room(form, request, game_name)
        else:
            return self.update_form_invalid(form, request, **kwargs)

    @staticmethod
    def create_room(form, request, game_name):
        form.save()
        room_name = form.data.get('room_name')
        room_url = reverse_lazy('room', args=[game_name, room_name])
        room_created.send(sender=LobbyView, action='Room created',
                          room_name=room_name, game_name=game_name, user=request.user)
        return HttpResponse(status=200, headers={
            'HX-Redirect': room_url
        })

    def update_form_invalid(self, form, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['field_name'] = 'room_name'
        return render(request, 'lobby/lobby_form.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Rooms.objects.all()
        context['rooms'] = rooms
        return context

    @staticmethod
    def join_room(request, game_name):
        try:
            room_name = request.GET.get('room-name')
            room = Rooms.objects.get(room_name=room_name)
            user = request.user
            user_joined_a_room.send(
                sender=LobbyView,
                action=f"{user.username} has left room {room_name}",
                room_name=room_name,
                user=user
            )
            if room.is_full:
                messages.success(request, 'Room is full')
                html = render_to_string('transcendence/messages_partial_update.html',
                                        context={'messages': messages.get_messages(request)})
                return HttpResponse(html, status=200, headers={
                    'HX-Retarget': '#alert-messages',
                })
            room_url = reverse_lazy('room', args=[game_name, room_name])
            print(room_url)
            return HttpResponse(status=200, headers={
                'HX-Redirect': room_url
            })
        except Rooms.DoesNotExist as e:
            raise Http404


class RoomView(LoginRequiredMixin, TemplateView):
    model = Rooms
    template_name = 'lobby/room.html'

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
        except Rooms.DoesNotExist:
            return redirect('lobby', kwargs['game_lobby'])
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')
            room_name = kwargs['room_name']
            game_name = kwargs['game_lobby']
            if hx_target == 'leave-room-btn':
                return RoomView.leave_room(room_name, game_name, request.user)
            if hx_target == 'play-game-btn':
                game_url = reverse_lazy('game', args=[game_name, room_name])
                start_game.send(sender=RoomView, action='Room created',
                                  room_name=room_name, game_name=game_name, user=request.user)
                return HttpResponse(status=200, headers={
                    'HX-Redirect': game_url
                })
        return render(request, self.template_name, context)

    @staticmethod
    def leave_room(room_name: str, game_name: str, user: AccountUser):
        user_left_a_room.send(
            sender=RoomView,
            action=f"{user.username} has left room {room_name}",
            room_name=room_name,
            user=user
        )
        return HttpResponse(status=200, headers={
            'HX-Redirect': reverse_lazy('lobby', args=[game_name])
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Rooms.objects.get(room_name=self.kwargs['room_name'])
        context['room'] = room
        context['room_name'] = room.room_name
        context['assigned_users'] = room.assigned_users.all()
        return context

    # # Used to select the normal or tournament room template
    # def get_template_names(self):
    #     return NotImplementedError
