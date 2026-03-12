from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User


# Create your views here.
@login_required(login_url="/login/")
def home(request):

    if request.user.status == User.Status.PENDING:
        return render(request, 'core/pending.html')
    if request.user.status == User.Status.REJECTED:
        return render(request, "core/rejected.html")
    if request.user.status == User.Status.BANNED:
        return render(request, "core/banned.html")

    context = {
        "authenticated": True,
        "user": request.user,
        "is_exec": False,
    }
    return render(request, 'core/home.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "core/login.html")
