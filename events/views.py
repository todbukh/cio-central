from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from core.permissions import is_executive
from django.shortcuts import render


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def events(request):
    context = {
        "active_tab": "events",
        "is_exec": is_executive(request.user)
    }

    return render(request, "events/events.html", context)