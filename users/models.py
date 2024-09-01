from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from users.managers import UserManager
from core.enums import UserType
from core.mixins import TimeStampMixin
from core.models import PossiblePhoneNumerField


class User(AbstractUser, PermissionsMixin, TimeStampMixin):
    """
    Model to represent users in platform
    """

    username = None

    email = models.EmailField(unique=True, max_length=255)

    second_last_name = models.CharField(max_length=100, null=False, blank=False)
    phone = PossiblePhoneNumerField(blank=True, default="")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=50,
        choices=[(type_name.upper(), type_name) for type_name, _ in UserType.CHOICES],
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"


class BlacklistedToken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
