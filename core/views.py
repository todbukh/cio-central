from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import User


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, "core/login.html")

@require_POST
@login_required
def delete_user(request, uid):
    user = get_object_or_404(User, uid=uid)
    user.delete()
    return redirect("/")