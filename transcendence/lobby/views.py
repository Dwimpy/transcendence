from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from .models import Rooms
from .forms import RoomForm
from accounts.models import AccountUser
# Create your views here.


# def lobby_view(request):
#     if request.method == 'POST':
#         print("POST POST POST")
#     test2, _ = Rooms.objects.get_or_create(room_name='test')
#     test1, _ = Rooms.objects.get_or_create(room_name='test1')
#     user1, _ = AccountUser.objects.get_or_create(username='andrei')
#     user2, _ = AccountUser.objects.get_or_create(username='danila')
#     test1.add_user_to_room(user1)
#     test1.add_user_to_room(user2)
#
#     if Rooms.is_user_assigned(user1) is False:
#         print('false')
#         test2.add_user_to_room(user1)
#     else:
#         print('true')
#     rooms = Rooms.objects.all()
#     return render(request, 'lobby/lobby.html', {'rooms': rooms})
#

class LobbyView(LoginRequiredMixin, ListView):
    model = Rooms
    form_class = RoomForm
    template_name = 'lobby/lobby.html'
    context_object_name = 'rooms'


class RoomProcessView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RoomForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        print("get")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM INVALID")
        return super().form_invalid(form)