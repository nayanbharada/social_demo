from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from .managers import CustomUserManager


# Create your models here.

class UserMaster(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
        default="",
    )
    email = models.EmailField(_("email address"), unique=True)
    friends = models.ManyToManyField("self", null=True, blank=True, related_name="user_friends")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def user_friends_count(self):
        return self.friends.count()