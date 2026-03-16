from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from django.shortcuts import render
from core.permissions import is_executive


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def roster(request):
    context = {
        "active_tab": "roster",
        "is_exec": is_executive(request.user)
    }

    return render(request, "roster/roster.html", context)