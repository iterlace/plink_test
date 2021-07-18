from typing import Any

from app.system.helpers import get_client_ip

from rest_framework import mixins, generics
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.serializers import Serializer

from authentication.models import SignUpRequest
from authentication.serializers import SignUpSerializer

from .renderers import DetailedRenderer


class SignUpRequestsList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = SignUpSerializer
    renderer_classes = [DetailedRenderer, BrowsableAPIRenderer]

    def get_queryset(self) -> QuerySet:
        ip = get_client_ip(self.request)
        qs = SignUpRequest.objects.filter(ip_addr=ip)
        return qs

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(ip_addr=get_client_ip(self.request))

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.create(request, *args, **kwargs)
