from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from .models import AccountUser
from .forms import ProfileForm
from .forms import RegistrationForm


# Create your views here.
class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = AccountUser
    form_class = ProfileForm

    def form_valid(self, form):
        return super().form_valid(form)


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


