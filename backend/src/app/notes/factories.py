import factory
import factory.fuzzy
from pytest_factoryboy import register

from django.utils import timezone

from authentication.factories import UserFactory

from .models import Note, NoteTag


@register
class NoteTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NoteTag
        django_get_or_create = ("owner", "name")

    owner = factory.SubFactory(UserFactory)
    name = factory.fuzzy.FuzzyText(length=5)
    date_added = factory.LazyAttribute(lambda _: timezone.now())


@register
class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    owner = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText(length=5)
    details = factory.fuzzy.FuzzyText(length=50)
    date_added = factory.LazyAttribute(lambda _: timezone.now())
    # TODO: tags
