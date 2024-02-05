import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from .models import Rooms
from .forms import RoomForm


# Create your views here.


class LobbyView(LoginRequiredMixin, ListView):
    model = Rooms
    form_class = RoomForm
    template_name = 'lobby/lobby.html'
    context_object_name = 'rooms'


class RoomProcessView(FormView):
    template_name = 'lobby/lobby_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('lobby')

    def form_valid(self, form):
        form.save()
        return HttpResponse(
            status=204,
            headers={
                'success': True,
                'HX-Trigger': json.dumps(
                    {
                        'roomAdded': None,
                        'success': True,
                    }
                )
            }
        )

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={'form': form}, status=400)


class UpdateRoomsView(View):

    def get(self, request, *args, **kwargs):
        rooms = Rooms.objects.all()
        html_to_string = render_to_string('lobby/lobby_room_partial.html', {'rooms': rooms})
        return HttpResponse(html_to_string, content_type='text/html',
                            status=200,
                            headers=
                            {
                                'success': True,
                            }
                        )
