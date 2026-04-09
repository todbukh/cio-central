from django.urls import path

from . import views

app_name = 'analytics'

urlpatterns = [
    path("", views.analytics, name="analytics"),
    path("users/<uuid:user_uid>/", views.user_detail, name="user_detail"),
]
