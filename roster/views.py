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
        context['members'] = User.objects.filter(status=User.Status.APPROVED).order_by("first_name", "last_name")
    elif active_roster == "applications":
         context["members"] = User.objects.filter(status=User.Status.PENDING).order_by("first_name", "last_name")
    elif active_roster == "banned-rejected":
        context["members"] = (User.objects.filter(status__in=[User.Status.BANNED, User.Status.REJECTED])
                              .order_by("first_name", "last_name"))

    return render(request, "roster/roster.html", context)

@require_POST
@executive_required(redirect_url="organization:home")
def accept(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.APPROVED
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="applications")

@require_POST
@executive_required(redirect_url="organization:home")
def reject(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.REJECTED
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="applications")

@require_POST
@executive_required(redirect_url="organization:home")
def ban(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.BANNED
    member.role = User.Role.MEMBER
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="members")

@require_POST
@executive_required(redirect_url="organization:home")
def renew_application(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.status = User.Status.PENDING
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="banned-rejected")

@require_POST
@owner_required(redirect_url="organization:home")
def set_role(request, pk):
    member = get_object_or_404(User, pk=pk)
    member.role = request.POST.get("role")
    member.save()
    return redirect("exec_panel:roster:roster", active_roster="members")