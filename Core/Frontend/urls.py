from django.urls import path, include

from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import FortyTwoProvider

urlpatterns = [
    path('', views.home, name='index'),
    path('text', views.text, name='text'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += default_urlpatterns(FortyTwoProvider)
