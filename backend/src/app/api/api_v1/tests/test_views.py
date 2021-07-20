import pytest

from django.urls import reverse
from django.test.client import Client
from rest_framework_simplejwt.tokens import RefreshToken

from notes.models import Note, NoteTag
from notes.factories import NoteFactory, NoteTagFactory
from authentication.models import User
from authentication.factories import UserFactory

from .mixins import ClientTestMixin


class TestSignUpView(ClientTestMixin):
    @pytest.mark.django_db
    def test_create_valid(self, client: Client) -> None:
        body = {
            "email": "john@foo.bar",
            "password": "Aasf12asf",
            "first_name": "John",
            "last_name": "Johnson",
        }
        response = self.post(client, url=reverse("api:v1:signup"), body=body)
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
        response = self.post(client, url=reverse("api:v1:signup"), body=body)
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    @pytest.mark.django_db
    def test_create_invalid(self, client: Client) -> None:
        body = {"email": "1"}
        response = self.post(client, url=reverse("api:v1:signup"), body=body)
        assert response.status_code == 400
        assert response.json()["status"] == "error"


class TestTokenEndpoints(ClientTestMixin):
    @pytest.mark.django_db
    def test_login(self, client: Client, user: User) -> None:
        body = {"email": user.email, "password": UserFactory.get_default_password()}
        response = self.post(
            client,
            url=reverse("api:v1:token_obtain_pair"),
            body=body,
        )
        assert response.status_code == 200
        assert set(response.json()["data"].keys()) == {"access", "refresh"}

    @pytest.mark.django_db
    def test_refresh(self, client: Client, user: User) -> None:
        refresh = RefreshToken.for_user(user)
        body = {"refresh": str(refresh)}
        response = self.post(
            client,
            url=reverse("api:v1:token_refresh"),
            body=body,
        )
        assert response.status_code == 200
        assert set(response.json()["data"].keys()) == {"access"}


class TestNoteViews(ClientTestMixin):
    @pytest.mark.django_db
    def test_retrieve(self, client: Client, note: Note) -> None:
        response = self.request(
            "get",
            client,
            url=reverse("api:v1:note_detail", args=(note.id,)),
            user=note.owner,
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete(self, client: Client, note: Note) -> None:
        response = self.request(
            "delete",
            client,
            url=reverse("api:v1:note_detail", args=(note.id,)),
            user=note.owner,
        )
        assert response.status_code == 204
        assert Note.objects.count() == 0

    @pytest.mark.django_db
    def test_put(self, client: Client, note: Note) -> None:
        body = {
            "title": "Lorem",
            "details": "lorem",
            "tags_names": [],
        }
        response = self.request(
            "put",
            client,
            url=reverse("api:v1:note_detail", args=(note.id,)),
            body=body,
            user=note.owner,
        )
        assert response.status_code == 200
        note.refresh_from_db()
        assert note.title == body["title"]
        assert note.details == body["details"]
        assert note.tags.count() == len(body["tags_names"])

    @pytest.mark.django_db
    def test_patch(self, client: Client, note: Note) -> None:
        body = {
            "title": "Lorem",
        }
        response = self.request(
            "patch",
            client,
            url=reverse("api:v1:note_detail", args=(note.id,)),
            body=body,
            user=note.owner,
        )
        assert response.status_code == 200
        note.refresh_from_db()
        assert note.title == body["title"]

    @pytest.mark.django_db
    def test_list(self, client: Client, user: User) -> None:
        count = 5
        for _ in range(count):
            NoteFactory(owner=user)

        response = self.request(
            "get",
            client,
            url=reverse("api:v1:notes"),
            user=user,
        )
        assert response.status_code == 200
        assert len(response.json()["data"]) == count

    @pytest.mark.django_db
    def test_create(self, client: Client, user: User) -> None:
        body = {
            "title": "Lorem",
            "details": "lorem",
            "tags_names": [],
        }

        response = self.request(
            "post",
            client,
            url=reverse("api:v1:notes"),
            body=body,
            user=user,
        )
        assert response.status_code == 201
        assert Note.objects.count() == 1


class TestNoteTagViews(ClientTestMixin):
    @pytest.mark.django_db
    def test_retrieve(self, client: Client, note_tag: NoteTag) -> None:
        response = self.get(
            client,
            url=reverse("api:v1:notes_tag_detail", args=(note_tag.name,)),
            user=note_tag.owner,
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete(self, client: Client, note_tag: NoteTag) -> None:
        response = self.delete(
            client,
            url=reverse("api:v1:notes_tag_detail", args=(note_tag.name,)),
            user=note_tag.owner,
        )
        assert response.status_code == 204
        assert NoteTag.objects.count() == 0

    @pytest.mark.django_db
    def test_list(self, client: Client, user: User) -> None:
        count = 5
        for _ in range(count):
            NoteTagFactory(owner=user)

        response = self.get(
            client,
            url=reverse("api:v1:notes_tags"),
            user=user,
        )
        assert response.status_code == 200
        assert len(response.json()["data"]) == count

    @pytest.mark.django_db
    def test_create(self, client: Client, user: User) -> None:
        body = {"name": "Lorem"}

        response = self.post(
            client,
            url=reverse("api:v1:notes_tags"),
            body=body,
            user=user,
        )
        assert response.status_code == 201
        assert NoteTag.objects.count() == 1
