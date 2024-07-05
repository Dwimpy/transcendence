from django.dispatch import Signal
from .handlers import (room_created_handler, user_joined_a_room_handler,
                       user_left_a_room_handler, delete_room_handler, start_game_handler)

room_created = Signal()
room_created.connect(room_created_handler)

user_joined_a_room = Signal()
user_joined_a_room.connect(user_joined_a_room_handler)

user_left_a_room = Signal()
user_left_a_room.connect(user_left_a_room_handler)

delete_room = Signal()
delete_room.connect(delete_room_handler)

start_game = Signal()
start_game.connect(start_game_handler)
