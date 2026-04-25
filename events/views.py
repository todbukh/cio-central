from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from core.decorators import executive_required
from django.views.decorators.http import require_POST

from organization.models import Channel, Message
from .forms import EventForm
from .models import Event


def _announcement_message_text(event):
    return f"Event: {event.name}\nView details: {reverse('events:event_detail_member', args=[event.uid])}"


# Main view to display all the events
@executive_required(redirect_url="organization:home")
def events(request, date_filter="all"):
    if date_filter == "today":
        all_events = Event.objects.filter(date__date=timezone.localdate())
    elif date_filter == "past":
        all_events = Event.objects.filter(date__lt=timezone.now())
    else:
        all_events = Event.objects.all()
    return render(request, "events/events.html", {
        "active_tab": "events",
        "events": all_events,
        "date_filter": date_filter,
    })

# Display details of a specific event (exec view)
@executive_required(redirect_url="organization:home")
def event_detail(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    return render(request, "events/event_detail.html", {"event": event, "active_tab": "events"})

# Member-facing event detail (no edit/delete, navbar only)
@login_required(login_url="/login/")
def event_detail_member(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    return render(request, "events/event_detail_member.html", {"event": event})

# Create a new event
@executive_required(redirect_url="organization:home")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, instance=Event(created_by=request.user))
        if form.is_valid():
            try:
                with transaction.atomic():
                    announcements_channel = Channel.objects.get(name="announcements")
                    event = form.save()
                    Message.objects.create(
                        channel=announcements_channel,
                        user=request.user,
                        text=_announcement_message_text(event),
                    )
            except Channel.DoesNotExist:
                form.add_error(None, "The announcements channel is missing.")
            except IntegrityError:
                form.add_error(None, "Could not post the event announcement. Please try again.")
            else:
                return redirect("exec_panel:events:events")
    else:
        form = EventForm()
    return render(request, "events/event_create.html", {"form": form, "active_tab": "events"})

# Edit an existing event
@executive_required(redirect_url="organization:home")
def event_edit(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("exec_panel:events:events")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_edit.html", {"form": form, "event": event, "active_tab": "events"})

# Display the delete confirmation page
@executive_required(redirect_url="organization:home")
def event_delete(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    return render(request, "events/event_delete.html", {"event": event, "active_tab": "events"})

# Perform the actual deletion (required to be a POST request for safety)
@executive_required(redirect_url="organization:home")
@require_POST
def event_delete_confirm(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    event.delete()
    return redirect("exec_panel:events:events")
