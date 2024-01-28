from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import AccountUser
from .forms import ProfileForm


# Create your views here.
class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/login.html'
    model = AccountUser
    form_class = ProfileForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

