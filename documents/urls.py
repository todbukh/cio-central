from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<uuid:file_uid>/", views.delete_file, name="delete_file"),
    path("delete/<uuid:file_uid>/confirm/", views.delete_file_post, name="delete_file_post"),
    path("view/<uuid:file_uid>/", views.view_document, name="view_document"),
]