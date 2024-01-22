from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta:
        app_label = 'frontend'
        db_table = 'users'

    bio = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def get_picture_url(self):
        return self.picture.url if hasattr(self, 'picture') and self.picture else None
