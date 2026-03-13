from django.urls import path

from . import views

app_name = 'exec_panel'

urlpatterns = [
    path("", views.executive_redirect, name="executive_redirect"),
    path("<str:tab>/", views.executive, name="executive"),
]