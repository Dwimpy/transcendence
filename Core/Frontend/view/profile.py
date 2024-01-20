from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..model.customuser import CustomUser
from django.shortcuts import render
from django.shortcuts import redirect
from ..form.profile import ProfileForm
from django.contrib.auth.decorators import login_required


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    model = CustomUser
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return f'/profile/' + self.request.user.username

    def form_invalid(self, form):
        return super().form_invalid(form)