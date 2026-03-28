from django.urls import path
from . import views

app_name = 'roster'

urlpatterns = [
    path("", views.roster, name="roster"),
    path("<str:active_roster>/", views.roster, name="roster"),
    path("action/accept/<uuid:uid>/", views.accept, name="accept"),
    path("action/reject/<uuid:uid>/", views.reject, name="reject"),
    path("action/ban/<uuid:uid>/", views.ban, name="ban"),
    path("action/renew_application/<uuid:uid>/", views.renew_application, name="renew_application"),
    path("set-role/<uuid:uid>/", views.set_role, name="set_role"),
    path("restore-application/<uuid:uid>/", views.restore_application, name="restore_application"),
]