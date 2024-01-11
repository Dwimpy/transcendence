from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'

    bio = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

