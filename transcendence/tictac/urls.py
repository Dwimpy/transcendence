from django.urls import path
from . import views

urlpatterns = [
    path('', views.tictacMainQ, name='tictacMainQ'),

    path('reset/', views.reset, name='reset'),
]