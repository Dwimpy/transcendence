from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class GameView(TemplateView):
    template_name = 'game/game.html'
    print("game view init")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request):
        print("hui")
        return render(request, self.template_name, status=200, context={})