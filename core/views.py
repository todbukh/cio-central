from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect


# Create your views here.
@login_required(login_url="/login/")
def home(request):
    context = {
        "authenticated": True,
        "user": request.user
    }

    return render(request, "core/index.html", context)

def login(request):
    if request.user.is_authenticated: return redirect("/")

    return render(request, "core/login.html")


@login_required(login_url="/login/")
def post_login_redirect(request):
    if request.user.is_exec:
        return redirect("executive")
    return redirect("home")


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.is_exec, login_url="/")
def executive_home(request):
    return render(request, "core/executive.html", {"user": request.user})