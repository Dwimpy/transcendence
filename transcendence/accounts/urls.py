from django.urls import path, include
from .views import (ProfileView, RegistrationView, FortyTwoAuthView, FortyTwoAuthCallbackView, UserLoginView, search_users, add_friend, remove_friend)
from django.contrib.auth import views as auth_view
from django.conf.urls import handler403
from django.shortcuts import render

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

handler403 = custom_403_view

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/42/', FortyTwoAuthView.as_view(), name='42_login'),
    path('login/42/callback/', FortyTwoAuthCallbackView.as_view(), name='42_callback'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),

    path('search/', search_users, name='search_users'),
    path('add_friend/<str:username>/', add_friend, name='add_friend'),
    path('remove_friend/<str:username>/', remove_friend, name='remove_friend'),
]
