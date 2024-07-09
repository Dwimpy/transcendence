from django.shortcuts import render

from django.views.generic import TemplateView


# Create your views here.
class LocalGameView(TemplateView):
    template_name = 'localgame/localgame.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("hui")
        return render(request, self.template_name, status=200, context={})


class LocalGameTournamentView(TemplateView):
    template_name = 'localgame/tournament.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("hui")
        return render(request, self.template_name, status=200, context={})