from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("<uuid:event_uid>/", views.event_detail_member, name="event_detail_member"),
]
