from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import UserAdminLoginForm
from django.contrib.auth import authenticate, login, logout

from core.models import User

def user_admin_login(request):
    # Claude Opus 4.6 Extended suggested request.user.is_authenticated guard to avoid error for anonymous users
    if request.user.is_authenticated and request.user.is_user_admin(): return redirect("user_admin:user_admin")

    if request.method == "POST":
        form = UserAdminLoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None and user.is_user_admin():
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


@require_POST
def user_admin_logout(request):
    # Claude Opus 4.6 Extended suggested adding this so crafted posts could not arbitrarily logout the user admin
    if not request.user.is_authenticated or not request.user.is_user_admin():
        raise PermissionDenied

    logout(request)
    return redirect("user_admin:login")


def user_admin(request):
    # redirect anonymous or non-USERADMIN users to the login page for this view
    if not request.user.is_authenticated or not request.user.is_user_admin(): return redirect("user_admin:login")

    context = {
        "members": User.objects.select_related("profile").order_by("first_name", "last_name"),
        "role_choices": User.Role.choices,  # Claude Opus 4.6 Extended showed me how to access these choices tuples
        "status_choices": User.Status.choices,
    }

    return render(request, "user_admin/user-admin.html", context)


@require_POST
def set_role(request, uid):
    # Deny ANY other user from setting roles
    if request.user.is_anonymous or request.user.role != User.Role.USERADMIN: raise PermissionDenied

    member = get_object_or_404(User, uid=uid)

    # other user admins (or themselves) cannot be modified
    if member.role == User.Role.USERADMIN: raise PermissionDenied

    new_role = request.POST.get("role")

    # No other user can be set to USERADMIN (also checks for crafted invalid roles)
    if new_role not in [User.Role.MEMBER, User.Role.EXEC, User.Role.OWNER]: raise PermissionDenied

    member.role = new_role
    member.save()

    return redirect("user_admin:user_admin")


@require_POST
def set_status(request, uid):
    # Deny ANY other user from setting status
    if request.user.is_anonymous or request.user.role != User.Role.USERADMIN: raise PermissionDenied

    member = get_object_or_404(User, uid=uid)

    # other user admins (or themselves) cannot be modified
    if member.role == User.Role.USERADMIN: raise PermissionDenied

    new_status = request.POST.get("status")

    # Prevents setting status to something invalid
    if new_status not in [User.Status.APPROVED, User.Status.PENDING, User.Status.REJECTED, User.Status.BANNED]:
        raise PermissionDenied

    member.status = new_status
    member.save()

    return redirect("user_admin:user_admin")
