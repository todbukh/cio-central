from django.urls import path
from . import views


app_name = "s3_demo"

urlpatterns = [
    path("", views.s3_demo, name="s3_demo"),
    path("delete/", views.s3_demo_delete, name="s3_demo_delete"),
]