from django.db import models
from accounts.models import AccountUser
# Create your models here.


class BaseConversation(models.Model):

    conversation_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivateConversation(BaseConversation):

    user1 = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    user2 = models.ForeignKey(AccountUser, on_delete=models.CASCADE)

