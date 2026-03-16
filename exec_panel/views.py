from django.contrib.auth.decorators import login_required, user_passes_test
from core.decorators import executive_required
from django.http.response import Http404
from django.shortcuts import render, redirect

@login_required(login_url="/login/")
@executive_required(redirect_url="core:home")
def executive_redirect(request):
    return redirect("exec_panel:executive", tab="roster")

@login_required(login_url="/login/")
@executive_required(redirect_url="core:home")
def executive(request, tab):
    defined_tabs = ["roster", "attendance", "analytics", "events"]

    if tab not in defined_tabs: raise Http404()

    exec_context = {
        "active_tab": tab
    }

    if tab == "roster":
        roster_context = {}
        return render(request, "exec_panel/roster.html", exec_context | roster_context)
    elif tab == "attendance":
        attendance_context = {}
        return render(request, "exec_panel/attendance.html", exec_context | attendance_context)
    elif tab == "analytics":
        analytics_context = {}
        return render(request, "exec_panel/analytics.html", exec_context | analytics_context)
    else:
        event_context = {}
        return render(request, "exec_panel/events.html", exec_context | event_context)