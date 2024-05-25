

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Game2
from django.utils import timezone

# Create your views here.
# class TictacView(TemplateView):
#     template_name = 'tictac/tictac.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, status=200, context={})
#
#     def post(self, request, *args, **kwargs):
#         return render(request, self.template_name, status=200, context={'messagess': 'wtf'})

    # saving result for user1 and user2
def update_game_history(user, game):
    if user.is_authenticated:
        history = user.history.get('tictac', [])
        game_record = {
            'game_name': 'tictac',
            'player1': user.username,
            'player2': None,  # Modify this if there's a second player
            'datetime': timezone.now().strftime('%Y-%m-%d %H:%M'),
            'winner': game.winner,
            'score': game.board  # Or any other scoring system you have
        }
        history.append(game_record)
        user.history['tictac'] = history
        user.save()

def tictacMainQ(request):
    game, created = Game2.objects.get_or_create(id=1)  # For simplicity, we use a single game instance

    if request.method == 'POST':
        index = int(request.POST.get('index'))
        if not game.is_over and game.board[index] == ' ':
            board = list(game.board)
            board[index] = game.current_turn
            game.board = ''.join(board)
            game.current_turn = 'O' if game.current_turn == 'X' else 'X'
            game.is_over, game.winner = check_winner(game.board)
            game.save()

            # saveResult()
            if game.is_over:
                update_game_history(request.user, game)

    # Create a list of tuples (index, value) for the board
    board_with_indices = [(i, game.board[i]) for i in range(9)]

    # Get the user's game history
    history = request.user.history.get('tictac', []) if request.user.is_authenticated else []

    context = {
        'game': game,
        'board_with_indices': board_with_indices,
        'history': history,
    }
    return render(request, 'tictac/tictac.html', context)


def reset(request):
    game = Game2.objects.get(id=1)
    game.board = ' ' * 9
    game.current_turn = 'X'
    game.is_over = False
    game.winner = None
    game.save()
    return redirect('tictac')


def check_winner(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)  # diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return True, board[combo[0]]
    if ' ' not in board:
        return True, 'Draw'
    return False, None