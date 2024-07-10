from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lobby.views import is_htmx
from lobby.signals import start_game
from .models import Game


# Create your views here.
class GameView(TemplateView):
    template_name = 'game/game.html'
    # print("game view init")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # print('hello')
        return render(request, self.template_name, status=200, context={"user": request.user})
