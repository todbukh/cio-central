from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import Http404
from django.shortcuts import render, redirect

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    return user.has_exec_access()

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def executive_redirect(request):
    return redirect("exec_panel:executive", tab="roster")

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def executive(request, tab):
    defined_tabs = ["roster", "attendance", "analytics", "events"]

    if tab not in defined_tabs: raise Http404()

    context = {
        "active_tab_classes": "bg-body shadow-sm text-body",
        "inactive_tab_classes": "text-body-secondary",
        "active_tab": tab
    }

    return render(request, "exec_panel/executive.html", context)