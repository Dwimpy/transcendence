from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.customuser import CustomUser
from ..forms.profile import ProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'frontend/profile.html'
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

