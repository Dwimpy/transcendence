from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .forms import ProfileForm
from .forms import AllAuthSignupForm

def register(request):
    if request.method == 'POST':
        form = AllAuthSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return redirect('index')  # Redirect to the home page after successful registration
    else:
        form = AllAuthSignupForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})


def text(response):
    return render(response, "text.html", {})


def home(response):
    return render(response, "home.html", {})
