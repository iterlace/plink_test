from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=100)

    password = serializers.CharField(
        min_length=7,
        max_length=16,
        validators=[
            RegexValidator(
                r"^[A-Z][a-zA-Z0-9_]*?$",
                "The password must begin with a capitalized letter, and contain only "
                "letters, digits and underscores.",
            )
        ],
    )

    first_name = serializers.CharField(
        validators=[
            RegexValidator(
                r"^[a-zA-Z\-]*$",
                "The first name must contain only letters and hyphens.",
            )
        ]
    )

    last_name = serializers.CharField(
        validators=[
            RegexValidator(
                r"^[a-zA-Z\- ]*$",
                "The last name must contain only letters, hyphens and spaces.",
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
