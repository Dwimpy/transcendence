from django.urls import path, include
from .views import ProfileView, RegistrationView, FortyTwoAuthView, FortyTwoAuthCallbackView, UserLoginView, search_users, add_friend
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/42/', FortyTwoAuthView.as_view(), name='42_login'),
    path('login/42/callback/', FortyTwoAuthCallbackView.as_view(), name='42_callback'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('search/', search_users, name='search_users'),
    path('add_friend/<str:username>/', add_friend, name='add_friend'),
]

