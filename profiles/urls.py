from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile_redirect, name="profile_redirect"),
    path("<str:username>/", views.profile_view, name="profile"),
]
