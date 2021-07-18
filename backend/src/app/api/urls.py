from django.urls import path, include

urlpatterns = [
    path(
        "v1/",
        include(("api.api_v1.urls", "api.api_v1"), namespace="v1"),
        name="v1",
    ),
]
