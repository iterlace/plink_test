from typing import Any

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from authentication.models import User

from .models import Note, NoteTag


class NoteTagSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:v1:notes_tag_detail",
        lookup_url_kwarg="name",
        lookup_field="name",
    )

    owner = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=User.objects.all(),
    )

    name = serializers.CharField(
        min_length=1,
        max_length=30,
    )

    date_added = serializers.DateTimeField(
        read_only=True,
    )

    class Meta:
        model = NoteTag
        fields = ("url", "owner", "name", "date_added")
        validators = [
            UniqueTogetherValidator(
                queryset=NoteTag.objects.all(),
                fields=["owner", "name"],
                message="You already have this tag!",
            )
        ]


class NoteSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:v1:note_detail",
        lookup_url_kwarg="id",
        lookup_field="id",
    )

    owner = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        queryset=User.objects.all(),
    )

    title = serializers.CharField(
        max_length=80,
    )

    details = serializers.CharField(
        required=False,
        default="",
    )

    date_added = serializers.DateTimeField(
        read_only=True,
    )

    tags = NoteTagSerializer(many=True, read_only=True)
    tags_names = serializers.SlugRelatedField(
        many=True,
        write_only=True,
        queryset=NoteTag.objects.none(),
        source="tags",
        slug_field="name",
    )

    def get_fields(self) -> Any:
        fields = super(NoteSerializer, self).get_fields()

        if hasattr(self, "initial_data"):
            fields["tags_names"].child_relation.queryset = NoteTag.objects.filter(  # type: ignore
                owner_id=self.initial_data["owner"],
            )
        return fields

    class Meta:
        model = Note
        fields = (
            "url",
            "owner",
            "title",
            "details",
            "date_added",
            "tags",
            "tags_names",
        )
