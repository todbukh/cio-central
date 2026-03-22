from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from django.shortcuts import render


@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def analytics(request):
    context = {
        "active_tab": "analytics"
    }

    return render(request, "analytics/analytics.html", context)