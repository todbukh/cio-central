from django.urls import path
from . import views

app_name = 'roster'

urlpatterns = [
    path("", views.roster_default),
    path("<str:tab>/", views.roster, name="roster"),
    path("action/accept/<int:pk>/", views.accept, name="accept"),
    path("action/reject/<int:pk>/", views.reject, name="reject"),
    path("action/ban/<int:pk>/", views.ban, name="ban"),
    path("action/renew_application/<int:pk>/", views.renew_application, name="renew_application"),
]