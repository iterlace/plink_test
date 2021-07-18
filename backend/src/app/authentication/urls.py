from authentication import views
from django.urls import path

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("requests", views.my_requests, name="my_requests"),
]
