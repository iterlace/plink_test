import json
from typing import Union

from django.http.response import JsonResponse
from django.test.client import Client
from django.urls import reverse


class TestSignUp:
    def get_url(self) -> str:
        return reverse("authentication:signup")  # type: ignore

    def post(
        self, client: Client, body: Union[Union[str, bytes], dict]
    ) -> JsonResponse:
        if isinstance(body, dict):
            body = json.dumps(body)
        response = client.post(self.get_url(), body, content_type="application/json")
        return response

    def test_valid(self, client: Client) -> None:
        body = {
            "email": "john@foo.bar",
            "password": "Aasf12asf",
            "first_name": "John",
            "last_name": "Johnson",
        }
        response = self.post(client, body)
        assert response.status_code == 200
        assert response.json() == {"error": False}

    def test_invalid_json(self, client: Client) -> None:
        body = b'{"email": '
        response = self.post(client, body)
        assert response.status_code == 400
        assert response.json() == {"error": True}

    def test_invalid_data(self, client: Client) -> None:
        body = {"email": "1"}
        response = self.post(client, body)
        assert response.status_code == 400
        assert response.json()["error"] is True
        assert response.json().get("details", None) is not None
