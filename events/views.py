from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from core.decorators import executive_required

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

# View to display details of a specific event
@executive_required(redirect_url="organization:home")
def event_detail(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    return render(request, "events/event_detail.html", {"event": event})

# View to create a new event
@executive_required(redirect_url="organization:home")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("exec_panel:events:events")
    else:
        form = EventForm()
    return render(request, "events/event_create.html", {"form": form})

# View to edit an existing event
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

# View to delete an event
@executive_required(redirect_url="organization:home")
def event_delete(request, event_uid):
    event = get_object_or_404(Event, uid=event_uid)
    if request.method == "POST":
        event.delete()
        return redirect("exec_panel:events:events")
    return render(request, "events/event_delete.html", {"event": event})
