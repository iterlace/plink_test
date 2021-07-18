from typing import Union

from django.http import HttpRequest
from rest_framework.request import Request as DRFRequest


def get_client_ip(request: Union[HttpRequest, DRFRequest]) -> str:
    ip: str
    if forwarded := request.META.get("HTTP_X_FORWARDED_FOR", None):
        ip = forwarded.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
