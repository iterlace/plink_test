from typing import Any, List

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        password: str,
        **kwargs: Any,
    ) -> "User":
        user = self.model(**kwargs)  # type: User
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password: str) -> "User":
        raise NotImplementedError()


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    first_name = models.TextField(
        _("first name"),
        null=False,
    )

    last_name = models.TextField(
        _("last name"),
        null=False,
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        null=False,
    )

    signup_ip_addr = models.GenericIPAddressField(
        _("ip address when registering"),
        null=False,
    )

    objects = UserManager()

    # this stuff is needed to use this model with django auth as a custom user class
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self) -> str:
        return "{}".format(self.email)

    class Meta:
        db_table = "authentication_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
