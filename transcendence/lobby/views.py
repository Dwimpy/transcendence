import json

from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from .consumers import LobbyConsumer
from .models import Rooms
from .forms import RoomForm
from channels.layers import get_channel_layer

# Create your views here.


class LobbyView(LoginRequiredMixin, TemplateView):
    model = Rooms
    form_class = RoomForm
    template_name = 'lobby/lobby.html'

