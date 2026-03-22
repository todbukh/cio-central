from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from django.shortcuts import render


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def events(request):
    context = {
        "active_tab": "events"
    }

    return render(request, "events/events.html", context)