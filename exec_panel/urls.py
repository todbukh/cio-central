from django.urls import path, include

from . import views

app_name = 'exec_panel'

urlpatterns = [
    path("", views.executive_redirect, name="executive_redirect"),
    path("events/", include("events.urls")),
    path("attendance/", include("attendance.urls")),
    path("analytics/", include("analytics.urls")),
    path("roster/", include("roster.urls")),
]