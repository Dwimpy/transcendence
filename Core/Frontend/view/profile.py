from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..model.customuser import CustomUser
from django.shortcuts import render
from django.shortcuts import redirect
from ..form.profile import ProfileForm
from django.contrib.auth.decorators import login_required


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = '../templates/profile.html'
    model = CustomUser
    form_class = ProfileForm
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user
