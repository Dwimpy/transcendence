from django.urls import path
from .views import HuiView

urlpatterns = [
    path('', HuiView.as_view(), name='hui')
]