
from django.dispatch import Signal
from .handlers import message_sent_handler, user_connected_handler

message_sent = Signal()
message_sent.connect(message_sent_handler)

user_connected = Signal()
user_connected.connect(user_connected_handler)