from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone

from attendance.models import Attendance
from core.decorators import executive_required
from core.models import User
from events.models import Event


def _build_chart_rows(rows, metric_key):
    if not rows:
        return []

    max_value = max(row[metric_key] for row in rows)

    return [
        {
            "label": row["name"],
            "value": row[metric_key],
            "percent": int((row[metric_key] / max_value) * 100) if max_value else 0,
        }
        for row in rows
    ]


def _format_rate(numerator, denominator):
    if not denominator:
        return "0%"
    return f"{round((numerator / denominator) * 100)}%"


def _build_user_detail_context(user):
    now = timezone.now()
    past_attendance = list(
        Attendance.objects
        .filter(member=user, event__date__lt=now)
        .select_related("event")
        .order_by("-event__date")
    )
    events_attended = sum(1 for row in past_attendance if row.status == Attendance.Status.PRESENT)
    tracked_events = len(past_attendance)
    display_name = user.get_full_name().strip() or user.username

    return {
        "active_tab": "analytics",
        "user_member": user,
        "display_name": display_name,
        "events_attended": events_attended,
        "tracked_events": tracked_events,
        "attendance_rate": _format_rate(events_attended, tracked_events),
        "attendance_rows": past_attendance,
    }


def _build_analytics_context(selected_view):
    now = timezone.now()
    past_events = Event.objects.filter(date__lt=now)
    approved_users = User.objects.filter(status=User.Status.APPROVED).exclude(role=User.Role.USERADMIN)

    past_events_with_counts = past_events.annotate(
        attendees=Count("attendance", filter=Q(attendance__status=Attendance.Status.PRESENT)),
        tracked_attendance=Count("attendance"),
    )
    all_past_events = sorted(past_events_with_counts, key=lambda event: event.date, reverse=True)
    recent_past_events = sorted(all_past_events, key=lambda event: event.date, reverse=True)[:3]
    past_event_count = past_events.count()

    total_present = sum(event.attendees for event in all_past_events)
    chart_rows = []
    for event in recent_past_events:
        tracked_count = event.tracked_attendance
        attendance_rate = _format_rate(event.attendees, tracked_count)
        chart_rows.append(
            {
                "name": event.name,
                "event_uid": event.uid,
                "attendees": event.attendees,
                "attendance_rate": attendance_rate,
            }
        )

    event_table_rows = []
    for event in all_past_events:
        tracked_count = event.tracked_attendance
        attendance_rate = _format_rate(event.attendees, tracked_count)
        event_table_rows.append(
            {
                "name": event.name,
                "event_uid": event.uid,
                "attendees": event.attendees,
                "attendance_rate": attendance_rate,
            }
        )

    user_rows = []
    approved_users_with_counts = approved_users.annotate(
        events_attended=Count(
            "attendance",
            filter=Q(
                attendance__event__date__lt=now,
                attendance__status=Attendance.Status.PRESENT,
            ),
        ),
        tracked_events=Count(
            "attendance",
            filter=Q(attendance__event__date__lt=now),
        ),
    ).order_by("-events_attended", "first_name", "last_name", "username")

    for user in approved_users_with_counts:
        tracked_events = user.tracked_events
        display_name = user.get_full_name().strip() or user.username
        user_rows.append(
            {
                "name": display_name,
                "user_uid": user.uid,
                "events_attended": user.events_attended,
                "attendance_rate": _format_rate(user.events_attended, tracked_events),
            }
        )

    avg_attendance = round(total_present / past_event_count) if past_event_count else 0
    summary_cards = [
        {"label": "Tracked members", "value": approved_users.count()},
        {"label": "Tracked events", "value": past_event_count},
        {"label": "Avg attendance", "value": avg_attendance},
    ]
    normalized_view = selected_view if selected_view in {"users", "events"} else "users"
    chart_rows = _build_chart_rows(chart_rows, "attendees") if normalized_view == "events" else []

    return {
        "active_tab": "analytics",
        "summary_cards": summary_cards,
        "selected_view": normalized_view,
        "chart_title": "Recent event turnout overview",
        "chart_rows": chart_rows,
        "table_title": "Per-user analytics" if normalized_view == "users" else "Per-event analytics",
        "table_rows": user_rows if normalized_view == "users" else event_table_rows,
    }


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def analytics(request):
    context = _build_analytics_context(request.GET.get("view", "users"))

    return render(request, "analytics/analytics.html", context)


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def user_detail(request, user_uid):
    user = get_object_or_404(User, uid=user_uid, status=User.Status.APPROVED)
    if user.role == User.Role.USERADMIN:
        raise Http404
    context = _build_user_detail_context(user)
    return render(request, "analytics/user_detail.html", context)
