from django.shortcuts import render
from .models import Rooms
from accounts.models import AccountUser
# Create your views here.


def lobby_view(request):
    test2, _ = Rooms.objects.get_or_create(room_name='test')
    test1, _ = Rooms.objects.get_or_create(room_name='test1')
    user1, _ = AccountUser.objects.get_or_create(username='andrei')
    user2, _ = AccountUser.objects.get_or_create(username='danila')
    test1.add_user_to_room(user1)
    test1.add_user_to_room(user2)
    if Rooms.is_user_assigned(user1) is False:
        print('false')
        test2.add_user_to_room(user1)
    else:
        print('true')
    rooms = Rooms.objects.all()
    return render(request, 'lobby/lobby.html', {'rooms': rooms})
