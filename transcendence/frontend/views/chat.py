from django.shortcuts import render
from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = 'frontend/chat.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
