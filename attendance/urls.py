from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path("", views.attendance, name="attendance"),
    path('<uuid:event_uid>/', views.event_attendance, name='event_attendance'),
    path('update/<uuid:event_uid>/<uuid:member_uid>/', views.update_attendance, name='update_attendance'),
]