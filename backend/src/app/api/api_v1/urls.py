from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    # Auth
    path(
        "authentication/signup/",
        views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "authentication/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "authentication/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # Notes
    path(
        "notes/",
        views.NoteListView.as_view(),
        name="notes",
    ),
    path(
        "notes/<int:id>/",
        views.NoteRetrieveView.as_view(),
        name="note_detail",
    ),
    path(
        "notes/tags/",
        views.NoteTagListView.as_view(),
        name="notes_tags",
    ),
    path(
        "notes/tags/<str:name>/",
        views.NoteTagRetrieveView.as_view(),
        name="notes_tag_detail",
    ),
]
