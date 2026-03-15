from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import Http404
from django.shortcuts import render, redirect

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    return user.is_exec()

def is_approved(user):
    return not user.is_anonymous and user.status == "APPROVED"

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def executive_redirect(request):
    return redirect("exec_panel:executive", tab="events")

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
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