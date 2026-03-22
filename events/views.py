from django.shortcuts import get_object_or_404, redirect, render
from core.decorators import executive_required
from django.views.decorators.http import require_POST

from .forms import EventForm
from .models import Event

# Main view to display all the events
@executive_required(redirect_url="organization:home")
def events(request):
    all_events = Event.objects.all()
    return render(request, "events/events.html", {
        "active_tab": "events",
        "events": all_events,
    })

# Display details of a specific event
@executive_required(redirect_url="organization:home")
def event_detail(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    return render(request, "events/event_detail.html", {"event": event})

# Create a new event
@executive_required(redirect_url="organization:home")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exec_panel:events:events")
    else:
        form = EventForm()
    return render(request, "events/event_create.html", {"form": form})

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
    return render(request, "events/event_edit.html", {"form": form, "event": event})

# Delete an event
@executive_required(redirect_url="organization:home")
@require_POST
def event_delete(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    if request.method == "POST":
        event.delete()
        return redirect("exec_panel:events:events")
    return render(request, "events/event_delete.html", {"event": event})
