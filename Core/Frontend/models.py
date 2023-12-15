# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     bio = models.TextField(blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name='customuser_set',
#         related_query_name='user',
#     )
#
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name='customuser_set',
#         related_query_name='user',
#     )
