from django.urls import path
from .views import LocalGameView

urlpatterns = [
    path('', LocalGameView.as_view(), name='localgame')
]