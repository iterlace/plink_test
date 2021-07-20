from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from authentication.models import User


class Note(models.Model):

    owner = models.ForeignKey(
        to=User,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        null=False,
    )

    title = models.TextField(
        _("title"),
        null=False,
    )

    details = models.TextField(
        _("details"),
        null=False,
        blank=True,
        default="",
    )

    date_added = models.DateTimeField(
        _("date added"),
        default=timezone.now,
        null=False,
    )

    tags = models.ManyToManyField(
        to="NoteTag",
        related_name="notes",
        db_table="notes_notes_tags",
    )

    class Meta:
        db_table = "notes_notes"


class NoteTag(models.Model):

    owner = models.ForeignKey(
        to=User,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        null=False,
    )

    name = models.TextField(
        _("name"),
        null=False,
    )

    date_added = models.DateTimeField(
        _("date added"),
        default=timezone.now,
        null=False,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "notes_tags"
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "name"),
                name="notes_tags_owner_name_key",
            )
        ]
