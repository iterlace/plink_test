import json
from typing import Any, Union

from django.urls import reverse
from django.test.client import Client
from django.http.response import JsonResponse

from authentication.models import SignUpRequest


class TestSignUpRequestsList:
    def get_url(self) -> str:
        return reverse("api:v1:signup")  # type: ignore

    def post(
        self, client: Client, body: Union[Union[str, bytes], dict]
    ) -> JsonResponse:
        if isinstance(body, dict):
            body = json.dumps(body)
        response = client.post(self.get_url(), body, content_type="application/json")
        return response

    def test_create_valid(self, client: Client, transactional_db: Any) -> None:
        body = {
            "email": "john@foo.bar",
            "password": "Aasf12asf",
            "first_name": "John",
            "last_name": "Johnson",
        }
        response = self.post(client, body)
        assert response.status_code == 201
        assert response.json()["status"] == "success"
        assert response.json()["data"] == body

    def test_create_invalid(self, client: Client, transactional_db: Any) -> None:
        body = {"email": "1"}
        response = self.post(client, body)
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    def test_list(self, client: Client, transactional_db: Any) -> None:
        entries_num = 5
        for _ in range(entries_num):
            # TODO: use factoryboy
            SignUpRequest.objects.create(
                ip_addr="127.0.0.1",
                email="john@foo.bar",
                password="123123123",
                first_name="John",
                last_name="Doe",
            )
        response = client.get(self.get_url())
        assert response.status_code == 200
        assert len(response.json()["data"]) == entries_num
