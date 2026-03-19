from django.urls import path

from . import views
from s3_demo.views import s3_demo

app_name = 'core'

urlpatterns = [
    path("login/", views.login, name="login"),
    path("s3demo/", s3_demo, name="s3_demo"),
]