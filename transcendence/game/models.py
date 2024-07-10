# pong/models.py
from django.db import models
from django.conf import settings

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1_games', on_delete=models.CASCADE)
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2_games', on_delete=models.CASCADE)
    # winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='won_games', on_delete=models.CASCADE, null=True, blank=True)
    # score_left = models.IntegerField(default=0)
    # score_right = models.IntegerField(default=0)
    # date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.game_id} - {self.player1.username} vs {self.player2.username}"
