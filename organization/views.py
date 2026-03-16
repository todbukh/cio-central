from django.contrib.auth.decorators import login_required
from core.permissions import is_pending, is_rejected, is_banned, is_executive
from django.shortcuts import render
from core.models import User


# Create your views here.
@login_required(login_url="/login/")
def home(request):

    if is_pending(request.user):
        return render(request, 'organization/pending.html')
    if is_rejected(request.user):
        return render(request, "organization/rejected.html")
    if is_banned(request.user):
        return render(request, "organization/banned.html")
    return render(request, 'organization/home.html', {
        "is_exec": is_executive(request.user)
    })
