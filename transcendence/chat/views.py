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
                    conversation = PrivateConversation.objects.filter(
                        Q(user1=user, user2=user2) | Q(user1=user2, user2=user)
                    ).first()

                    if not conversation:
                        conversation = PrivateConversation.objects.create(
                            user1=user, user2=user2
                        )
                        conversation = PrivateConversation.objects.filter(
                            Q(user1=user, user2=user2) | Q(user1=user2, user2=user)
                        ).first()
                    print(conversation)
                    content_type = ContentType.objects.get_for_model(conversation)
                    context['messages'] = Messages.objects.filter(content_type=content_type,
                                                                  object_id=conversation.pk)
                    context['user'] = request.user
                    context['other'] = user2.username
                    context['initial'] = user2.username[0].capitalize()
                    context['hidden'] = ""
                    return render(request, 'chat/chat_window.html', context)
                except AccountUser.DoesNotExist:
                    raise Http404
        user = AccountUser.objects.get(username=request.user)
        context = self.get_context_data(**kwargs)
        context['friends'] = user.friends
        context['hidden'] = "hidden"
        return render(request, self.template_name, status=200, context=context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, status=200, context={'messagess': 'wtf'})
