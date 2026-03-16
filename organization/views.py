from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import User


# Create your views here.
@login_required(login_url="/login/")
def home(request):

    if request.user.status == User.Status.PENDING:
        return render(request, 'organization/pending.html')
    if request.user.status == User.Status.REJECTED:
        return render(request, "organization/rejected.html")
    if request.user.status == User.Status.BANNED:
        return render(request, "organization/banned.html")
    return render(request, 'organization/home.html')
