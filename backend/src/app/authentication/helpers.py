import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods


def get_client_ip(request: HttpRequest) -> str:
    if forwarded := request.META.get("HTTP_X_FORWARDED_FOR", None):
        ip = forwarded.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
