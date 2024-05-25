# game/models.py
from django.db import models

class Game2(models.Model):
    board = models.CharField(max_length=9, default=' ' * 9)  # 9 characters for the board
    current_turn = models.CharField(max_length=1, default='X')  # 'X' or 'O'
    is_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=1, blank=True, null=True)

