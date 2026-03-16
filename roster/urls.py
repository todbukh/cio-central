from django.urls import path

from . import views

app_name = 'roster'

urlpatterns = [
    path("", views.roster, name="roster"),
    path("action/accept/<int:pk>/", views.accept, name="accept"),
    path("action/reject/<int:pk>/", views.reject, name="reject"),
    path("action/ban/<int:pk>/", views.ban, name="ban"),
]