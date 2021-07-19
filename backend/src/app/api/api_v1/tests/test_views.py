import json
from typing import Union

import pytest

from django.urls import reverse
from django.test.client import Client
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.factories import UserFactory


class TestSignUpView:
    def get_url(self) -> str:
        return reverse("api:v1:signup")

    def post(
        self, client: Client, body: Union[Union[str, bytes], dict]
    ) -> JsonResponse:
        if isinstance(body, dict):
            body = json.dumps(body)
        response = client.post(self.get_url(), body, content_type="application/json")
        return response  # type: ignore

    @pytest.mark.django_db
    def test_create_valid(self, client: Client) -> None:
        body = {
            "email": "john@foo.bar",
            "password": "Aasf12asf",
            "first_name": "John",
            "last_name": "Johnson",
        }
        response = self.post(client, body)
        assert response.status_code == 201
        assert response.json()["status"] == "success"
        assert response.json()["data"] == {"email": body["email"]}

    @pytest.mark.django_db
    def test_create_duplicated(self, client: Client, user: User) -> None:
        body = {
            "email": user.email,
            "password": "Aasf12asf",
            "first_name": "John",
            "last_name": "Johnson",
        }
        response = self.post(client, body)
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    @pytest.mark.django_db
    def test_create_invalid(self, client: Client) -> None:
        body = {"email": "1"}
        response = self.post(client, body)
        assert response.status_code == 400
        assert response.json()["status"] == "error"


class TestTokenEndpoints:
    @pytest.mark.django_db
    def test_login(self, client: Client, user: User) -> None:
        body = {"email": user.email, "password": UserFactory.get_default_password()}
        response = client.post(
            reverse("api:v1:token_obtain_pair"),
            json.dumps(body),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert set(response.json()["data"].keys()) == {"access", "refresh"}

    @pytest.mark.django_db
    def test_refresh(self, client: Client, user: User) -> None:
        refresh = RefreshToken.for_user(user)
        body = {"refresh": str(refresh)}
        response = client.post(
            reverse("api:v1:token_refresh"),
            json.dumps(body),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert set(response.json()["data"].keys()) == {"access"}
