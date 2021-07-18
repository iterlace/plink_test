from django.urls import path, include

urlpatterns = [
    path(
        "api/",
        include(("api.urls", "api"), namespace="api"),
        name="api",
    ),
    path(
        "authentication/",
        include(("authentication.urls", "authentication"), namespace="authentication"),
        name="authentication",
    ),
]
