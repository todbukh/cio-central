from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path("", views.user_admin, name="user_admin"),
    path("login/", views.user_admin_login, name="login"),
    path("logout/", views.user_admin_logout, name="logout"),
    path("set-role/<uuid:uid>/", views.set_role, name="set_role"),
    path("set-status/<uuid:uid>/", views.set_status, name="set_status")
]