from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=200, context={'messagess': [
            'Hello bro',
            'How are you ?'
        ]})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, status=200, context={'messagess': 'wtf'})
