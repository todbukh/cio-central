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

@login_required(login_url='/login/')
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def roster_default(request):
    return redirect("exec_panel:roster:roster", tab="members")

@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def roster(request, tab="members"):
    context = {
        "active_tab": tab
    }
    if tab == "members":
        members = User.objects.filter(status=User.Status.APPROVED)
        sorted_members = [request.user]
        sorted_members += list(members.exclude(pk=request.user.pk).order_by("first_name", "last_name"))
        context['members'] = sorted_members
    elif tab == "applications":
         context["members"] = User.objects.filter(status=User.Status.PENDING).order_by("first_name", "last_name")
    elif tab == "banned-rejected":
        context["members"] = User.objects.filter(status__in=[User.Status.BANNED, User.Status.REJECTED]).order_by("first_name", "last_name")

    return render(request, "roster/roster.html", context)

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def accept(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.APPROVED
    member.save()
    return redirect("exec_panel:roster:roster", tab="applications")

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def reject(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.REJECTED
    member.save()
    return redirect("exec_panel:roster:roster", tab="applications")

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def ban(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.BANNED
    member.role = User.Role.MEMBER
    member.save()
    return redirect("exec_panel:roster:roster", tab="members")

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def renew_application(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.PENDING
    member.save()
    return redirect("exec_panel:roster:roster", tab="banned-rejected")

@require_POST
@login_required(login_url="/login/")
@user_passes_test(is_owner, login_url="/", redirect_field_name=None)
def set_role(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.role = request.POST.get("role")
    member.save()
    return redirect("exec_panel:roster:roster", tab="members")