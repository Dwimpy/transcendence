from channels.db import database_sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta:
        app_label = 'frontend'
        db_table = 'users'

    bio = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='frontend/profile_pics/', blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'bio': self.bio,
            'email': self.email
        }

    def get_picture_url(self):
        return self.picture.url if hasattr(self, 'picture') and self.picture else None

    @database_sync_to_async
    def get_user_by_username(self, name):
        return CustomUser.objects.get(username=name)
