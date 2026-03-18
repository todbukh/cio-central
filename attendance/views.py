from enum import member

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core.models import User
from .models import Attendance
from events.models import Event

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    return user.is_exec()

def is_approved(user):
    return not user.is_anonymous and user.status == "APPROVED"

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def attendance(request):
    events = Event.objects.all().order_by("date")
    context = {
        "active_tab": "attendance",
        "events": events,
    }

    return render(request, "attendance/attendance.html", context)

def event_attendance(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    existing_attendance_member_ids = Attendance.objects.filter(event=event).values_list("member_id", flat=True)
    new_attendance_members = User.objects.filter(status=User.Status.APPROVED).exclude(id__in=existing_attendance_member_ids)
    if new_attendance_members:
        new_records = [
            Attendance(event=event, member=member, status=Attendance.Status.UNSET) for member in new_attendance_members
        ]
        Attendance.objects.bulk_create(new_records)
    context = {
        "active_tab": "attendance",
        "attendees": Attendance.objects.filter(event=event).select_related("member").order_by("member__last_name"),
        "event": event,
    }
    return render(request, "attendance/event_attendance.html", context)

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def update_attendance(request, event_pk, member_pk):
    attendance = get_object_or_404(Attendance, event_id=event_pk, member_id=member_pk)
    attendance.status = request.POST["status"]
    attendance.save()
    return redirect("exec_panel:attendance:event_attendance", event_id=event_pk)