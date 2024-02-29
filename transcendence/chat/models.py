from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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

    user1 = models.ForeignKey(AccountUser, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(AccountUser, related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Private conversation between {self.user1} and {self.user2}'


class GroupConversation(BaseConversation):

    group_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(AccountUser, related_name='group_conversations')

    def __str__(self):
        return f'Group conversation {self.group_name}'


class Messages(models.Model):

    message_id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    sender = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.content} from {self.sender}'

