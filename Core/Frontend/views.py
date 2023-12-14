from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.


def text(response):
    return render(response, "text.html", {})


def home(response):
    return render(response, "home.html", {})
