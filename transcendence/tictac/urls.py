from django.urls import path
from . import views

urlpatterns = [
    path('', views.tictacMainQ, name='tictac'),

    path('reset/', views.reset, name='reset'),
]