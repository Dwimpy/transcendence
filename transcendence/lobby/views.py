import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Rooms
from .forms import RoomForm


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
                Rooms.update_lobby()
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
            return LobbyView.create_room(form, request)
        else:
            return self.update_form_invalid(form, request, **kwargs)

    @staticmethod
    def create_room(form, request):
        form.save()
        room_name = form.data.get('room_name')
        room = Rooms.objects.get(room_name=room_name)
        room.add_user_to_room(request.user)
        room.save()
        Rooms.update_lobby()
        room_url = reverse_lazy('room', args=[room_name])
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
    def join_room(request):
        try:
            room_name = request.GET.get('room-name')
            room = Rooms.objects.get(room_name=room_name)
            if room.is_full:
                messages.success(request, 'Room is full')
                html = render_to_string('transcendence/messages_partial_update.html',
                                        context={'messages': messages.get_messages(request)})
                return HttpResponse(html, status=200, headers={
                    'HX-Retarget': '#alert-messages',
                })
            room.add_user_to_room(request.user)
            Rooms.update_lobby()
            room_url = reverse_lazy('room', args=[room_name])
            return HttpResponse(status=200, headers={
                'HX-Redirect': room_url
            })
        except Rooms.DoesNotExist as e:
            raise Http404


class RoomView(LoginRequiredMixin, TemplateView):
    model = Rooms
    template_name = 'lobby/room.html'

    def get(self, request, *args, **kwargs):
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')
            room_name = kwargs['room_name']
            if hx_target == 'leave-room-btn':
                return RoomView.leave_room(room_name, request.user)
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    @staticmethod
    def leave_room(room_name: str, user):
        try:
            room = Rooms.objects.get(room_name=room_name)
            room.remove_user_from_room(user)
            Rooms.update_lobby()
            return HttpResponse(status=200, headers={
                'HX-Redirect': reverse_lazy('lobby')
            })
        except Rooms.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Rooms.objects.get(room_name=self.kwargs['room_name'])
        context['room'] = room
        context['room_name'] = room.room_name
        context['assigned_users'] = room.assigned_users.all()
        return context
