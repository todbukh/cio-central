from django.urls import path
from . import views

app_name = "organization"

urlpatterns = [
    path("messsaging/<str:channel>/", views.home, name="home"),
]