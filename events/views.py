from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.
def is_exec(user):
    if user.is_anonymous: return False
    return user.is_exec()

def is_approved(user):
    return not user.is_anonymous and user.status == "APPROVED"

@login_required(login_url="/login/")
@user_passes_test(is_approved, login_url="/", redirect_field_name=None)
@user_passes_test(is_exec, login_url="/", redirect_field_name=None)
def events(request):
    context = {
        "active_tab": "events"
    }

    return render(request, "events/events.html", context)