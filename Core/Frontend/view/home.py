from django.views import View
from django.shortcuts import render


class HomeView(View):
	template_name = '../templates/home.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
