from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from .models import AccountUser
from .forms import ProfileForm
from .forms import RegistrationForm
from django.shortcuts import render


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
        print("WTF")
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


