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

    def get(self, *args, **kwargs):
        try:
            user = self.get_object()
            form = self.form_class(instance=user)
            return render(self.request, self.template_name, {'user': user, 'form': form})
        except AccountUser.DoesNotExist:
            raise Http404("User does not exist")

    def form_valid(self, form):
        return super().form_valid(form)


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


