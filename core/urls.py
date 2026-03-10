from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("post-login/", views.post_login_redirect, name="post_login_redirect"),
    path("executive/", views.executive_home, name="executive"),
]