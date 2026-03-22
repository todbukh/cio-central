from django.urls import path
from . import views

app_name = "organization"

urlpatterns = [
    # this redirects "/" to "/messages/general/"
    path("", views.home_redirect, name="home"),  # kept this as "organization:home" to avoid refactoring
    path("messages/delete/", views.delete_message, name="delete_message"),
    path("messages/create-channel/", views.create_channel, name="create_channel"),
    path("messages/<slug:channel>/edit/", views.edit_channel, name="edit_channel"),
    path("messages/<slug:channel>/delete/", views.delete_channel, name="delete_channel"),
    path("messages/<slug:channel>/", views.messages, name="messages")
]