from django.urls import path, include
from .views import HomeView

urlpatterns = [
    path(r'', HomeView.as_view(), name='index')
]