from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.exec_polls, name="polls"),
    path("create/", views.exec_poll_create, name="poll_create"),
    path("<uuid:poll_uid>/", views.exec_poll_detail, name="poll_detail"),
    path("<uuid:poll_uid>/close/", views.exec_poll_close, name="poll_close"),
]
