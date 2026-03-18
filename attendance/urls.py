from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path("", views.attendance, name="attendance"),
    path('<int:event_id>/', views.event_attendance, name='event_attendance'),
    path('update/<int:event_pk>/<int:member_pk>/', views.update_attendance, name='update_attendance'),
]