from django.urls import path, re_path, include
from .views import ProfileView, RegistrationView
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration')

]