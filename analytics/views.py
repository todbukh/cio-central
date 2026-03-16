from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from core.permissions import is_executive
from django.shortcuts import render


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def analytics(request):
    context = {
        "active_tab": "analytics",
        "is_exec": is_executive(request.user)
    }

    return render(request, "analytics/analytics.html", context)