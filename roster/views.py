from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from core.models import User

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    return user.is_exec()

def is_approved(user):
    return not user.is_anonymous and user.status == "APPROVED"

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def roster(request, tab):
    context = {
        "active_tab": tab
    }
    if tab == "roster":
         context["members"] = User.objects.filter(status="APPROVED")
    elif tab == "applications":
         context["members"] = User.objects.filter(status="PENDING")
    elif tab == "banned/rejected":
        context["members"] = User.objects.filter(status__in=["BANNED", "REJECTED"])

    return render(request, "roster/roster.html", context)