from django.contrib.auth.decorators import login_required
from core.decorators import executive_required
from core.permissions import is_executive
from django.shortcuts import render



@login_required(login_url="/login/")
@executive_required(redirect_url="organization:home")
def attendance(request):
    context = {
        "active_tab": "attendance"
    }

    return render(request, "attendance/attendance.html", context)