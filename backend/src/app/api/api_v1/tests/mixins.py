import json
from typing import Any, Union, Literal, Optional

from django.test.client import Client
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


class ClientTestMixin:
    def request(
        self,
        method: Literal["get", "post", "put", "patch", "delete"],
        client: Client,
        url: str,
        user: Optional[User] = None,
        body: Optional[Union[Union[str, bytes], dict]] = None,
    ) -> JsonResponse:
        kwargs = {}
        if user is not None:
            token = RefreshToken.for_user(user).access_token
            kwargs["HTTP_AUTHORIZATION"] = "Bearer {}".format(str(token))
        if body is not None:
            kwargs["content_type"] = "application/json"
            if isinstance(body, dict):
                body = json.dumps(body)
            kwargs["data"] = body  # type: ignore

        callable_ = getattr(client, method)
        response = callable_(url, **kwargs)
        return response  # type: ignore

    def get(self, *args: Any, **kwargs: Any) -> JsonResponse:
        return self.request("get", *args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> JsonResponse:
        return self.request("post", *args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> JsonResponse:
        return self.request("put", *args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> JsonResponse:
        return self.request("patch", *args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> JsonResponse:
        return self.request("delete", *args, **kwargs)
