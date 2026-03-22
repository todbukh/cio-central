from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="events"),
    path("create/", views.event_create, name="event_create"),
    path("<uuid:event_uid>/", views.event_detail, name="event_detail"),
    path("<uuid:event_uid>/edit/", views.event_edit, name="event_edit"),
    path("<uuid:event_uid>/delete/", views.event_delete, name="event_delete")
]
