from typing import Any, Dict

from django.conf import settings
from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="The user with this email is already " "registered.",
            )
        ],
    )

    password = serializers.CharField(
        min_length=7,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^[A-Z][a-zA-Z0-9_]*?$",
                message="The password must begin with a capitalized letter, and contain only "
                "letters, digits and underscores.",
            )
        ],
        write_only=True,
    )

    first_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\-]*$",
                message="The first name must contain only letters and hyphens.",
            )
        ]
    )

    last_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\- ]*$",
                message="The last name must contain only letters, hyphens and spaces.",
            )
        ]
    )

    def validate_email(self, value: str) -> str:
        domain = value.split("@")[-1].strip()
        if domain in settings.EMAIL_DOMAINS_BLACKLIST:
            raise serializers.ValidationError(
                "Your email's domain is blacklisted. Please use another one."
            )
        return value

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super(SignUpSerializer, self).update(instance, validated_data)  # type: ignore

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
