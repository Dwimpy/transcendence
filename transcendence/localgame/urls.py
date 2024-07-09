from django.urls import path
from .views import LocalGameView, LocalGameTournamentView

urlpatterns = [
    path('', LocalGameView.as_view(), name='localgame'),
    path('tournament/', LocalGameTournamentView.as_view(), name='tournament')
]