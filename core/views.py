from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User
from core.permissions import is_banned, is_executive, is_pending, is_rejected


# Create your views here.
@login_required(login_url="/login/")
def home(request):

    if is_pending(request.user):
        return render(request, 'core/pending.html')
    if is_rejected(request.user):
        return render(request, "core/rejected.html")
    if is_banned(request.user):
        return render(request, "core/banned.html")

    context = {
        "authenticated": True,
        "user": request.user,
        "is_exec": is_executive(request.user),
    }
    return render(request, 'core/home.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "core/login.html")
