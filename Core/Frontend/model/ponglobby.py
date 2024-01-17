from django.db import models
from enum import Enum
from django.utils.translation import gettext as _
from Frontend.model.customuser import CustomUser
import uuid


def generate_lobby_name():
    return str(uuid.uuid4().hex[:8])


class PongLobby(models.Model):
    class LobbyState(models.TextChoices):
        LOBBY = 'W', _('Waiting')
        PLAYING = 'P', _('Playing')
        FINISHED = 'F', _('Finished')

    class Meta:
        db_table = 'pong_lobbies'

    lobby_id = models.UUIDField(uuid.uuid4, editable=False, unique=True, default=uuid.uuid4())
    name = models.CharField(max_length=255, default=None)
    state = models.CharField(max_length=1, choices=LobbyState.choices, default=LobbyState.LOBBY)
    users = models.ManyToManyField(CustomUser, related_name='lobbies')
    player_count = models.IntegerField(default=0)
    lobby_full = models.BooleanField(default=False)

    def add_to_lobby(self, username):
        if self.lobby_full is True:
            return
        self.player_count += 1
        self.users.add(username)
        if self.player_count == 2:
            self.lobby_full = True

    def __str__(self):
        return f'id: {self.lobby_id}\nstate: {self.state}'

