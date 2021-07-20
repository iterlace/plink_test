from typing import Any

from app.system.helpers import get_client_ip

from rest_framework import mixins, status, generics, permissions
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from notes.models import Note, NoteTag
from notes.serializers import NoteSerializer, NoteTagSerializer
from authentication.serializers import SignUpSerializer


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

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


class NoteListView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        super(NoteListView, self).initial(request, *args, **kwargs)
        request.data["owner"] = request.user.id

    def get_queryset(self) -> QuerySet[Note]:
        return Note.objects.filter(owner=self.request.user)  # type: ignore


class NoteRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        super(NoteRetrieveView, self).initial(request, *args, **kwargs)
        request.data["owner"] = request.user.id

    def get_queryset(self) -> QuerySet[NoteTag]:
        return Note.objects.filter(owner=self.request.user)  # type: ignore


class NoteTagListView(generics.ListCreateAPIView):
    serializer_class = NoteTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        super(NoteTagListView, self).initial(request, *args, **kwargs)
        request.data["owner"] = request.user.id

    def get_queryset(self) -> QuerySet[NoteTag]:
        return NoteTag.objects.filter(owner=self.request.user)  # type: ignore


class NoteTagRetrieveView(
    mixins.DestroyModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = NoteTagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "name"
    lookup_field = "name"

    def get_queryset(self) -> QuerySet[NoteTag]:
        return NoteTag.objects.filter(owner=self.request.user)  # type: ignore

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.destroy(request, *args, **kwargs)
