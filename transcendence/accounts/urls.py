from django.urls import path, include
from .views import ProfileView, RegistrationView, FortyTwoAuthView, FortyTwoAuthCallbackView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/42/', FortyTwoAuthView.as_view(), name='42_login'),
    path('login/42/callback/', FortyTwoAuthCallbackView.as_view(), name='42_callback'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<str:pk>/', ProfileView.as_view(), name='profile'),
]

