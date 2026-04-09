from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path("", views.user_admin, name="user_admin"),
    path("login/", views.user_admin_login, name="login"),
]