from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def post(self, request, *args, **kwargs):
        print(self.request.body)
        return render(request, self.template_name, status=204)
