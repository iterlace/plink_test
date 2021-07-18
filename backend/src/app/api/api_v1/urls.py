from django.urls import path

from . import views

urlpatterns = [
    path("authentication/signup", views.SignUpRequestsList.as_view(), name="signup"),
]
