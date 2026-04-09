from django.shortcuts import render, redirect
from .forms import UserAdminLoginForm
from django.contrib.auth import authenticate, login, logout

def user_admin_login(request):
    # Claude Opus 4.6 Extended suggested request.user.is_authenticated guard to avoid error for anonymous users
    if request.user.is_authenticated and request.user.is_user_admin(): return redirect("user_admin:user_admin")

    if request.method == "POST":
        form = UserAdminLoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                if request.user.is_authenticated:  # logout if a user was already logged-in with another account
                    logout(request)

                login(request, user)
                return redirect("user_admin:user_admin")
            else:
                # Claude Opus 4.6 Extended suggested adding this error to display to the user on an invalid login attempt
                form.add_error(None, "Invalid username or password.")

    else:
        form = UserAdminLoginForm()

    context = {
        "form": form
    }

    return render(request, "user_admin/user-admin-login.html", context)

def user_admin(request):
    context = {}

    return render(request, "user_admin/user-admin.html", context)