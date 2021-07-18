from django.db.models import (
    Model,
    AutoField,
    TextField,
    EmailField,
    GenericIPAddressField,
)


class SignUpRequest(Model):
    id = AutoField(primary_key=True)

    ip_addr = GenericIPAddressField()

    email = EmailField()
    password = TextField()
    first_name = TextField()
    last_name = TextField()

    class Meta:
        db_table = "signup_requests"
        verbose_name = "Sign-up request"
        verbose_name_plural = "Sign-up requests"
