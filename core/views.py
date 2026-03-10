from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User


# Create your views here.
@login_required(login_url="/login/")
def home(request):

    if request.user.status == User.Status.PENDING:
        return render(request, 'core/pending.html')
    if request.user.status == User.Status.REJECTED:
        return render(request, "core/rejected.html", )
    if request.user.status == User.Status.BANNED:
        return render(request, "core/banned.html")
    is_exec = request.user.role in [User.Role.OWNER, User.Role.EXEC]
    context = {
        "authenticated": True, # ask about this
        "user": request.user,
        "is_exec": is_exec,
    }
    return render(request, 'core/home.html', context)

@login_required(login_url="/login/")
def executive_page(request):
    pass

def login(request):
    if request.user.is_authenticated: return redirect("/")
    return render(request, "core/login.html")