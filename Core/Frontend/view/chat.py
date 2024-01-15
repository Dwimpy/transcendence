from django.shortcuts import render
from django.views import View


class ChatView(View):
	template_name = '../templates/chat.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})