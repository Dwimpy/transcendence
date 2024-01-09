# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'

    bio = models.CharField()
    picture = models.ImageField(upload_to='images/', blank=True, null=True)

