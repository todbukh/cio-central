from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core.models import User

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    if user.status != User.Status.APPROVED: return False
    return user.is_exec()

def is_owner(user):
    if not is_exec(user):
        return False
    return user.role == User.Role.OWNER

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def roster(request, tab):
    context = {
        "active_tab": tab
    }
    if tab == "roster":
         context["members"] = User.objects.filter(status="APPROVED")
    elif tab == "applications":
         context["members"] = User.objects.filter(status="PENDING")

    return render(request, "roster/roster.html", context)

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
@require_POST
def accept(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.APPROVED
    member.save()
    return redirect("roster:roster", tab="applications")

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
@require_POST
def reject(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.REJECTED
    member.save()
    return redirect("roster:roster", tab="roster")

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
@require_POST
def ban(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.BANNED
    member.save()
    return redirect("roster:roster", tab="roster")