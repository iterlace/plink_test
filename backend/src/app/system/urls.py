from django.urls import include, path

urlpatterns = [
    path(
        "authentication/",
        include(("authentication.urls", "authentication"), namespace="authentication"),
        name="authentication",
    ),
    # path("admin/", admin.site.urls),
]
