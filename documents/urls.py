from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:file_id>/", views.delete_file, name="delete_file"),
    path("view/<int:file_id>/", views.view_document, name="view_document"),
]