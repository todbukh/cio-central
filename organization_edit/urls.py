from django.urls import path
from . import views

app_name = "organization-edit"

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.edit, name="edit"),
]