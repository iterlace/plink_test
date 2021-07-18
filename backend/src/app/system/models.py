from typing import List, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManagerCustom(BaseUserManager):
    def create_user(
        self,
        password: Optional[str] = None,
        is_superuser: bool = False,
        is_staff: bool = False,
        is_active: bool = True,
    ) -> "User":
        user: "User" = self.model()  # noqa

        user.set_password(password)  # change password to hash
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    # system field
    username = models.CharField(
        _("username"),
        max_length=30,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$",
                _(
                    "Enter a valid username. This value may contain only letters, "
                    "numbers and @/./+/-/_ characters."
                ),
                "invalid",
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"),
        unique=False,
        blank=True,
        null=True,
        error_messages={
            "unique": "Користувач з такою електронною поштою вже існує",
        },
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
    )

    objects = UserManagerCustom()

    # this stuff is needed to use this model with django auth as a custom user class
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self) -> str:
        return "{}".format(self.username)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
