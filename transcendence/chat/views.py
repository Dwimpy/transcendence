from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import AccountUser
from lobby.views import is_htmx
from .models import PrivateConversation, Messages
# Create your views here.
from django.db.models import Q


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get(self, request, *args, **kwargs):
        if is_htmx(request):
            hx_target = request.headers.get('HX-Target')
            if hx_target == 'chat-window-container':
                context = self.get_context_data(**kwargs)
                user: AccountUser = request.user
                other_user_name = request.GET.get("other")
                try:
                    user2: AccountUser = AccountUser.objects.get(username=other_user_name)
                    conversation: PrivateConversation = PrivateConversation.objects.filter(
                        Q(user1__username=user.username, user2__username=user2.username) |
                        Q(user1__username=user2.username, user2__username=user.username)
                    ).first()
                    content_type = ContentType.objects.get_for_model(conversation)
                    context['messages'] = Messages.objects.filter(content_type=content_type,
                                                                  object_id=conversation.pk)
                    context['other'] = user2.username
                    context['initial'] = user2.username[0].capitalize()
                    return render(request, 'chat/chat_window.html', context)
                except AccountUser.DoesNotExist:
                    raise Http404
        return render(request, self.template_name, status=200, context={})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, status=200, context={'messagess': 'wtf'})
