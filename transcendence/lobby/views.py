import json

from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .consumers import LobbyConsumer
from .models import Rooms
from .forms import RoomForm
from channels.layers import get_channel_layer
from .constants import LOBBY_WS_GROUP_NAME

# Create your views here.

def is_htmx(request):
    return request.META.get('HTTP_HX_REQUEST') is not None


class LobbyView(LoginRequiredMixin, TemplateView):
    model = Rooms
    form_class = RoomForm
    template_name = 'lobby/lobby.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')
            if hx_target == 'lobby_room':
                Rooms.update_rooms()
            elif hx_target == 'dialog':
                context['field_name'] = 'room_name'
                context['form'] = RoomForm()
                return render(request, 'lobby/lobby_form.html', context)
            elif hx_target == 'join-room-btn':
                return LobbyView.join_room(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RoomForm(request.POST)
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')

        if form.is_valid():
            form.save()
            room_name = form.data.get('room_name')
            room_url = reverse_lazy('room', args=[room_name])
            Rooms.update_rooms()
            return HttpResponse(status=200, headers={
                'HX-Redirect': room_url
            })
        else:
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
    def join_room(request):
        room_name = request.GET.get('room-name')
        room_url = reverse_lazy('room', args=[room_name])
        return HttpResponse(status=200, headers={
            'HX-Redirect': room_url
        })


class RoomView(LoginRequiredMixin, TemplateView):
    model = Rooms
    template_name = 'lobby/room.html'

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Rooms.objects.get(room_name=self.kwargs['room_name'])
        context['room_name'] = room.room_name
        context['assigned_users'] = room.assigned_users.all()
        return context
