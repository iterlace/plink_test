from typing import Any, Optional

import factory
from factory import Faker
from pytest_factoryboy import register

from .models import User


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    _DEFAULT_PASSWORD = "admin"

    email = Faker("ascii_safe_email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    signup_ip_addr = Faker("ipv4")
    is_superuser = False

    @factory.post_generation
    def password(self, create: bool, extracted: Optional[str], **kwargs: Any) -> None:
        if not create:
            return
        if extracted is not None:
            self.set_password(extracted)
        else:
            self.set_password(UserFactory._DEFAULT_PASSWORD)

    @classmethod
    def get_default_password(cls) -> str:
        return cls._DEFAULT_PASSWORD
