from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<str:file_name>/", views.delete_file, name="delete_file"),
    path("view/<str:filename>/", views.view_document, name="view_document"),
]