from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from core.models import User
from core.decorators import executive_required, owner_required

# Create your views here.
@executive_required(redirect_url="organization:home")
def roster(request, active_roster="members"):
    context = {
        "active_tab": "roster",
        "active_roster": active_roster,
    }
    if active_roster == "members":
        context['members'] = (User.objects
                              .filter(status=User.Status.APPROVED)
                              .exclude(role=User.Role.USERADMIN)
                              .order_by("first_name", "last_name"))
    elif active_roster == "applications":
         context["members"] = (User.objects
                               .filter(status=User.Status.PENDING)
                               .exclude(role=User.Role.USERADMIN)
                               .order_by("first_name", "last_name"))
    elif active_roster == "banned-rejected":
        context["members"] = (User.objects
                              .filter(status__in=[User.Status.BANNED, User.Status.REJECTED])
                              .exclude(role=User.Role.USERADMIN)
                              .order_by("first_name", "last_name"))

    return render(request, "roster/roster.html", context)

@require_POST
@executive_required(redirect_url="organization:home")
def accept(request, uid):
    member = get_object_or_404(User, uid=uid)
    member.status = User.Status.APPROVED
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="applications")

@require_POST
@executive_required(redirect_url="organization:home")
def reject(request, uid):
    member = get_object_or_404(User, uid=uid)
    member.status = User.Status.REJECTED
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="applications")

@require_POST
@executive_required(redirect_url="organization:home")
def ban(request, uid):
    member = get_object_or_404(User, uid=uid)
    if member.role == User.Role.EXEC and request.user.role != User.Role.Owner:
        raise PermissionDenied
    member.status = User.Status.BANNED
    member.role = User.Role.MEMBER
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="members")

@require_POST
@executive_required(redirect_url="organization:home")
def renew_application(request, uid):
    member = get_object_or_404(User, uid=uid)
    member.status = User.Status.PENDING
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="banned-rejected")

@require_POST
@owner_required(redirect_url="organization:home")
def set_role(request, uid):
    member = get_object_or_404(User, uid=uid)
    member_role = request.POST.get("role")
    if member_role not in [User.Role.EXEC, User.Role.MEMBER]:
        raise PermissionDenied
    member.role = member_role
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="members")

@require_POST
@login_required(login_url="/login/")
def restore_application(request, uid):
    if request.user.uid != uid or request.user.status == User.Status.BANNED:
        raise PermissionDenied
    member = get_object_or_404(User, uid=uid)
    member.status = User.Status.PENDING
    member.save()
    return redirect("organization:home")