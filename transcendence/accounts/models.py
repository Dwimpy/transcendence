from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


gettext_lazy = lazy(gettext, str)


# Create your models here.
class AccountUser(AbstractUser):
    class Meta:
        app_label = 'accounts'
        db_table = 'users'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        primary_key=True
    )
    bio = models.CharField(max_length=255, default="")
    picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)


