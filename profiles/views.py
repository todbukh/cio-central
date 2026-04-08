from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from core.permissions import is_executive, is_owner
from project_a_17.settings import DELETED_USER_UID
from .forms import ProfileEditForm
from django.core.files.storage import default_storage

User = get_user_model()

@login_required(login_url="/login/")
def profile_redirect(request):
    return redirect("profiles:profile", username=request.user.username)

@login_required(login_url="/login/")
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user.status != "APPROVED":
        raise Http404
    user_is_profile_owner =  request.user == profile_user
    context = {
        "profile_user": profile_user,
        "is_executive": is_executive(request.user),
        "user_is_profile_owner": user_is_profile_owner,
        "can_delete": is_owner(request.user) or (is_executive(request.user) and not is_executive(profile_user)) or user_is_profile_owner,
    }
    return render(request, "profiles/profile.html", context)

@login_required(login_url="/login/")
def profile_edit_view(request, username):
    if request.user.username != username: # only allow users to edit their own profile
        return redirect("profiles:profile", username=username)

    profile = request.user.profile

    if request.method == "POST": # user wants to save changes to profile
        if "delete_picture" in request.POST: # user clicks delete button to clear profile picture
            if profile.profile_picture:
                profile.profile_picture.delete()
            return redirect("profiles:profile", username = username)
        profile_picture_file_name = None
        if 'profile_picture' in request.FILES and profile.profile_picture:
            profile_picture_file_name = profile.profile_picture.name # use of .name to pass in string

        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if profile_picture_file_name: default_storage.delete(profile_picture_file_name)
            form.save()
            return redirect("profiles:profile", username=username)
    else:                       # user just wants to view the edit page
        form = ProfileEditForm(instance=profile)

    return render(request, "profiles/profile_edit.html", {"form": form, "profile_user": request.user})

@require_POST
@login_required
def delete_user(request, username):
    member = get_object_or_404(User, username=username)
    if request.user.is_exec() or request.user == member:
        member.delete()
    else:
        return HttpResponseForbidden()
    return redirect("/")