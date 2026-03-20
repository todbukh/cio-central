from django.urls import path
from . import views

app_name = "organization"

urlpatterns = [
    # this redirects "/" to "/messages/general/"
    path("", views.home_redirect, name="home"),  # kept this as "organization:home" to avoid refactoring
    path("messages/<str:channel>/", views.messages, name="messages"),
]