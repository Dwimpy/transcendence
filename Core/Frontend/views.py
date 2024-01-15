import requests
from django.shortcuts import render, redirect
from .view.auth42 import oauth2_login
from .view.auth42 import oauth2_callback
