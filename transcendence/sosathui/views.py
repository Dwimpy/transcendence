from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HuiView(TemplateView):
    template_name = 'hui/hui.html'
    # print("game view init")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request):
        # print("hui")
        return render(request, self.template_name, status=200, context={})