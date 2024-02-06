from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from .models import AccountUser
from .forms import ProfileForm
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.conf import settings
from urllib.parse import quote
import requests
from django.contrib import messages


# Create your views here.
class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = AccountUser
    form_class = ProfileForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            logged_user = self.request.user
            user = self.get_object()
            form = self.form_class(instance=user)
            if not logged_user.username == user.username:
                for field in form.fields:
                    form.fields[field].widget.attrs['readonly'] = True
            return render(self.request, self.template_name, {'user': user,
                                                             'logged_user': logged_user.username,
                                                             'form': form})
        except AccountUser.DoesNotExist:
            raise Http404("User does not exist")

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        url = reverse_lazy('profile', args=[user.username])
        return url


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user=user)
        return super().form_valid(form)


class FortyTwoAuthView(View):

    def get(self, request):
        authorize_url = 'https://api.intra.42.fr/oauth/authorize'
        print(settings.REDIRECT_URI)
        redirect_uri = quote(settings.REDIRECT_URI, safe='')
        scope = 'public'
        response_type = 'code'
        return redirect(f'{authorize_url}?'
                        f'client_id={settings.CLIENT_ID}&'
                        f'redirect_uri={redirect_uri}&'
                        f'response_type={response_type}&'
                        f'scope={scope}')


class FortyTwoAuthCallbackView(View):

    def __init__(self, *args, **kwargs):
        self.access_token = None
        super().__init__(*args, **kwargs)

    def get(self, request):
        self.access_token = FortyTwoAuthCallbackView.get_auth_token(self.request)
        if self.access_token:
            user_data = self.get_user_data().json()
            user_login = user_data['login']
            if not AccountUser.objects.filter(username=user_login).exists():
                user_nickname = user_data['displayname']
                user_email = user_data['email']
                user_bio = user_data['kind']
                user = AccountUser.objects.create(username=user_login,
                                           email=user_email,
                                           bio=user_bio,
                                           nickname=user_nickname)
                login(request, user)
                return redirect('profile', user.username)
            else:
                user = AccountUser.objects.get(username=user_login)
                login(request, user)
        return redirect('index')

    @staticmethod
    def get_auth_token(request):
        token_url = 'https://api.intra.42.fr/oauth/token'
        code = request.GET.get('code')
        if code:
            token_data = {
                'grant_type': 'authorization_code',
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET,
                'redirect_uri': settings.REDIRECT_URI,
                'code': request.GET.get('code')
            }
            response = requests.post(token_url, data=token_data,
                                     headers={
                                         'Content-Type': 'application/x-www-form-urlencoded'
                                     }).json()
            token = response.get('access_token')
            if token:
                return token
            else:
                messages.info(request, response['error_message'])
        messages.info(request, 'Invalid authorization code')
        return None

    def get_user_data(self):
        profile_url = 'https://api.intra.42.fr/v2/me'
        user_data = requests.get(profile_url,
                                 headers={
                                     'Authorization': f'Bearer {self.access_token}'
                                 })
        return user_data

    @staticmethod
    def extract_login_details(self):
        pass