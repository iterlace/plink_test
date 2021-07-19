from typing import Any

from app.system.helpers import get_client_ip

from rest_framework import status, generics
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.serializers import SignUpSerializer

from .renderers import DetailedRenderer

User = get_user_model()


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    renderer_classes = [DetailedRenderer, BrowsableAPIRenderer]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(signup_ip_addr=get_client_ip(self.request))

        response_serializer = TokenObtainPairSerializer(
            {
                "email": request.data["email"],
                "password": request.data["password"],
            },
            context={"request": request},
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
