from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from core.permissions import is_executive
from .forms import ProfileEditForm

User = get_user_model()

@login_required(login_url="/login/")
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

@login_required(login_url="/login/")
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_owner =  request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_owner": is_owner
    }
    return render(request, "profiles/profile.html", context)

@login_required(login_url="/login/")
def profile_edit_view(request, username):
    if request.user.username != username: # only allow users to edit their own profile
        return redirect("profiles:profile", username=username)

    profile = request.user.profile

    if request.method == "POST": # user wants to save changes to profile
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile", username=username)
    else:                       # user just wants to view the edit page
        form = ProfileEditForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form})
