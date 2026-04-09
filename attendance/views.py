import datetime

from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core.decorators import executive_required
from core.models import User
from .models import Attendance
from events.models import Event

# Create your views here.
@executive_required(redirect_url="organization:home")
def attendance(request, date_filter="today"):
    if date_filter in ["all", "ALL"]:
        events = Event.objects.all().order_by("date")
    else: events = Event.objects.filter(date__date=timezone.localdate())
    context = {
        "active_tab": "attendance",
        "events": events,
        "date_filter": date_filter,
    }

    return render(request, "attendance/attendance.html", context)

@executive_required(redirect_url="organization:home")
def event_attendance(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    existing_attendance_member_ids = Attendance.objects.filter(event=event).values_list("member_id", flat=True)
    new_attendance_members = User.objects.filter(status=User.Status.APPROVED).exclude(id__in=existing_attendance_member_ids)
    if new_attendance_members:
        new_records = []
        for member in new_attendance_members:
            if not member.is_user_admin():  # does not lazily create attendance records for USERADMINs
                new_records.append(Attendance(event=event, member=member, status=Attendance.Status.UNSET))

        Attendance.objects.bulk_create(new_records)
    context = {
        "active_tab": "attendance",
        "attendees": Attendance.objects.filter(event=event).exclude(member__role=User.Role.USERADMIN).select_related("member").order_by("member__last_name"),
        "event": event,
    }
    return render(request, "attendance/event_attendance.html", context)

@require_POST
@executive_required(redirect_url="organization:home")
def update_attendance(request, event_uid, member_uid):
    member_attendance = get_object_or_404(Attendance, event__uid=event_uid, member__uid=member_uid)
    member_attendance_status = request.POST["status"]
    if member_attendance_status not in [Attendance.Status.PRESENT, Attendance.Status.ABSENT, Attendance.Status.UNSET, Attendance.Status.EXCUSED]:
        raise PermissionDenied("Status doesn't exist")
    member_attendance.status = member_attendance_status
    member_attendance.save()
    return redirect("exec_panel:attendance:event_attendance", event_uid=event_uid)